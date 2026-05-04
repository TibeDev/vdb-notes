#!/usr/bin/env bash
set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo: sudo $0"
    exit 1
fi

# Check python3
command -v python3 >/dev/null || { echo "Error: python3 not found"; exit 1; }

# Check source file
[ -f "./app.py" ] || { echo "Error: app.py not found"; exit 1; }

# Create directories
mkdir -p /usr/local/bin /usr/local/share/notes-cli

# Install files
cp ./app.py /usr/local/share/notes-cli/
chmod +x /usr/local/share/notes-cli/app.py

# Create launcher
cat > /usr/local/bin/notes <<EOF
#!/usr/bin/env bash
exec python3 /usr/local/share/notes-cli/app.py "\$@"
EOF

chmod +x /usr/local/bin/notes

echo "Run with: notes"

#YES THIS IS INSTALL SCRIPT IS MADE WITH AI.