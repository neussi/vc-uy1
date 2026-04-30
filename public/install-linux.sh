#!/bin/bash

# VC-UY1 : RESEARCH AGENT LINUX BOOTSTRAP (V3.2)
# Developed by Antigravity for University of Yaoundé 1

set -e

echo "--------------------------------------------------------"
echo "  UNIVERSITY OF YAOUNDE 1 - RESEARCH NODE INSTALLER     "
echo "--------------------------------------------------------"

# 1. Prerequisites Check
echo "[1/4] Checking environment..."
if ! python3 -m venv --help &> /dev/null; then
    echo "Python3 venv is not installed. Attempting to install..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
fi

# 2. Dependency Resolution
echo "[2/4] Resolving research dependencies..."
INSTALL_DIR="$HOME/.vc-uy1-agent"
mkdir -p "$INSTALL_DIR"

echo "Creating secure virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install psutil requests certifi

# 3. Agent Fetching (Source-based to avoid GLIBC issues)
echo "[3/4] Pulling latest agent source..."
cd "$INSTALL_DIR"

# Download source files from the distribution hub
wget -q -O collector.py https://vc-uy1.npe-techs.com/agent/collector.py
wget -q -O syncer.py https://vc-uy1.npe-techs.com/agent/syncer.py
wget -q -O workload.py https://vc-uy1.npe-techs.com/agent/workload.py
wget -q -O main.py https://vc-uy1.npe-techs.com/agent/main.py
wget -q -O persistence.py https://vc-uy1.npe-techs.com/agent/persistence.py
wget -q -O heartbeat.py https://vc-uy1.npe-techs.com/agent/heartbeat.py

# 4. Persistence Setup
echo "[4/4] Activating research persistence..."
mkdir -p "$HOME/.config/systemd/user/"

cat <<EOF > "$HOME/.config/systemd/user/vc-agent.service"
[Unit]
Description=VC-UY1 Research Node (Persistent)
After=network.target

[Service]
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/main.py --foreground
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable vc-agent.service
systemctl --user restart vc-agent.service

echo "--------------------------------------------------------"
echo " SUCCESS: Your node is now contributing to the cluster! "
echo " Check your contribution on: https://vc-uy1.npe-techs.com "
echo "--------------------------------------------------------"
