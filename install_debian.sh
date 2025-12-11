#!/usr/bin/env bash
# filepath: /tmp/install_easy_print_scan.sh
set -euo pipefail

APP_USER="easyprint"              # change or set to "$USER" if you don't want a separate user
APP_DIR="/opt/easy-print-scan-server"
REPO_URL="https://github.com/dodo8/easy-print-scan-server.git"  # change if needed
PYTHON_VERSION="python3"

echo "=== Updating package lists ==="
sudo apt-get update -y

echo "=== Installing base system packages ==="
sudo apt-get install -y \
    $PYTHON_VERSION python3-venv python3-pip \
    git \
    cups cups-bsd \
    sane-utils

echo "=== Enabling and starting CUPS service ==="
sudo systemctl enable cups
sudo systemctl start cups

# Optional: add current user to lpadmin and scanner groups for admin/scan access
CURRENT_USER="$(whoami)"
echo "=== Adding $CURRENT_USER to lpadmin and scanner groups (log out/in to take effect) ==="
sudo usermod -aG lpadmin "$CURRENT_USER" || true
sudo usermod -aG scanner "$CURRENT_USER" || true

echo "=== Creating application user (if needed) ==="
if ! id -u "$APP_USER" >/dev/null 2>&1; then
    sudo useradd -m -s /bin/bash "$APP_USER"
fi

echo "=== Cloning or updating repository ==="
if [ ! -d "$APP_DIR/.git" ]; then
    sudo mkdir -p "$APP_DIR"
    sudo chown "$APP_USER":"$APP_USER" "$APP_DIR"
    sudo -u "$APP_USER" git clone "$REPO_URL" "$APP_DIR"
else
    sudo -u "$APP_USER" bash -lc "cd '$APP_DIR' && git pull --rebase || true"
fi

echo "=== Creating Python virtual environment and installing dependencies ==="
sudo -u "$APP_USER" bash -lc "
    cd '$APP_DIR' &&
    $PYTHON_VERSION -m venv venv &&
    source venv/bin/activate &&
    # Install requirements but ignore pywin32 if present (Windows-only)
    if grep -qi 'pywin32' requirements.txt; then
        sed '/pywin32/Id' requirements.txt > requirements.linux.txt
        pip install --no-cache-dir -r requirements.linux.txt
    else
        pip install --no-cache-dir -r requirements.txt
    fi
"

cat <<'EOF'

============================================================
 Installation complete.

 NEXT STEPS:

 1) Configure CUPS (printing):
    - On this server:
        sudo lpstat -p
    - Optionally from a browser (if accessible):
        http://<server-ip>:631
      Add your printer and print a test page.

 2) Configure SANE (scanning):
    - List scanners:
        scanimage -L
    - Copy the device string (e.g. 'epson2:libusb:001:004')
      into config/config.yaml under scanning.unix_device_name.

 3) Run the app:
    - As APP_USER:
        sudo -u easyprint bash -lc '
            cd /opt/easy-print-scan-server &&
            source venv/bin/activate &&
            python run.py
        '
    - Open the printed URL (default http://127.0.0.1:7860)
      or expose the port to your network.

 4) Remember:
    - You were added to lpadmin and scanner groups.
      Log out and back in for group changes to take effect.

============================================================
EOF