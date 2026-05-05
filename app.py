#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

menu = ["New File", "Find File"]
file_tasks = ["Edit", "Delete"]

notes_dir = Path.home() / ".vdb-notes"
notes_dir.mkdir(exist_ok=True)

def ShowList(options, prompt, no_input):
    cmd = ["fzf", "--prompt", prompt]

    if no_input:
        cmd.append("--no-input")

    result = subprocess.run(
        cmd,
        input="\n".join(options),
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def ShowMenu():
    choice = ShowList(menu, "",True)

    if choice is None:
        sys.exit(0)

    if choice == "Find File":
        FindFile()
    elif choice == "New File":
        NewFile()


def EditFile(file):
    result = subprocess.run(
        ["nano", f"{notes_dir}/{file}"]
    )
    ShowMenu()


def DeleteFile(file):
    confirm = ShowList(["Yes", "No"], "You sure wanna delete this file?",True)

    if confirm is None or confirm == "No":
        ShowMenu()
        return

    if confirm == "Yes":
        os.remove(f"{notes_dir}/{file}")
        ShowMenu()


def NewFile():
    result = subprocess.run(
        ["fzf", "--prompt=New file > ", "--print-query"],
        input="",
        text=True,
        capture_output=True
    )

    lines = result.stdout.splitlines()
    file_name = lines[0].strip() if lines else ""

    if not file_name:
        ShowMenu()
        return

    full_path = f"{notes_dir}/{file_name}.txt"

    if os.path.exists(full_path):
        print("That file already exists")
        ShowMenu()
    else:
        EditFile(file_name + ".txt")


def FindFile():
    files = subprocess.run(
        ["ls", notes_dir],
        text=True,
        capture_output=True
    )

    notes = files.stdout.strip().split("\n") if files.stdout.strip() else []

    note_choice = ShowList(notes, "",False)
    if note_choice is None:
        ShowMenu()
        return

    file_task = ShowList(file_tasks, "",True)
    if file_task is None:
        ShowMenu()
        return

    if file_task == "Edit":
        EditFile(note_choice)
    elif file_task == "Delete":
        DeleteFile(note_choice)


def main():
    ShowMenu()


if __name__ == "__main__":
    main()