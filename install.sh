#!/usr/bin/env bash

set -e

SCRIPT_NAME="notes"
INSTALL_PATH="/usr/local/bin/$SCRIPT_NAME"
SOURCE_PATH="$(pwd)/app.py"

echo "Installing $SCRIPT_NAME..."

# Check if script exists
if [ ! -f "$SOURCE_PATH" ]; then
    echo "Error: notes.py not found in current directory"
    exit 1
fi

# Copy to system bin
sudo cp "$SOURCE_PATH" "$INSTALL_PATH"

# Make executable
sudo chmod +x "$INSTALL_PATH"

# Ensure python shebang exists
if ! head -n 1 "$INSTALL_PATH" | grep -q "^#!"; then
    echo "Adding python shebang..."
    sudo sed -i '1i #!/usr/bin/env python3' "$INSTALL_PATH"
fi

echo "Installed successfully!"
echo "Run it with: $SCRIPT_NAME"

#YES THIS IS FULLY WRITTEN BY AI LIKE WHAT YOU GONNA BE MAD