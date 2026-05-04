import subprocess
import sys
import os

NOTES_DIR = os.path.expanduser("~/.local/share/vdb-notes/notes")

os.makedirs(NOTES_DIR, exist_ok=True)

files = subprocess.run(
    ["ls", NOTES_DIR],
    capture_output=True,
    text=True
)

notes = files.stdout.strip().split("\n") if files.stdout.strip() else []

result = subprocess.run(
    "printf '%s\n' " + " ".join(notes) + " | fzf --print-query",
    shell=True,
    capture_output=True,
    text=True
)

if result.returncode == 130:
    sys.exit(0)

lines = result.stdout.strip().split("\n")
query = lines[0] if lines else ""

if not query:
    sys.exit(0)

file_path = (
    f"{NOTES_DIR}/{query}"
    if query in notes
    else f"{NOTES_DIR}/{query}.txt"
)

subprocess.run(["nano", file_path])