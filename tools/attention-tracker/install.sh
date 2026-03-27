#!/usr/bin/env bash
# Attention Tracker — local install script
# Run this on your Linux desktop (not in DevSpaces)
#
# Usage: bash install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.local/share/attention-tracker"
CONFIG_DIR="$HOME/.config/attention-tracker"
SYSTEMD_DIR="$HOME/.config/systemd/user"

echo "=== Attention Tracker Installer ==="
echo ""

# 1. Install the Python package
echo "[1/5] Installing Python package..."
cd "$SCRIPT_DIR"
pip install --user -e ".[dev]" 2>/dev/null || pip install -e ".[dev]"
echo "  done"

# 2. Create data directory
echo "[2/5] Creating data directory..."
mkdir -p "$INSTALL_DIR"
echo "  $INSTALL_DIR"

# 3. Copy default rules if no custom rules exist
echo "[3/5] Setting up classification rules..."
mkdir -p "$CONFIG_DIR"
if [ ! -f "$CONFIG_DIR/rules.toml" ]; then
    cp "$SCRIPT_DIR/attention_tracker/default_rules.toml" "$CONFIG_DIR/rules.toml"
    echo "  Default rules copied to $CONFIG_DIR/rules.toml"
    echo "  Edit this file to customize categories for your workflow"
else
    echo "  Custom rules already exist at $CONFIG_DIR/rules.toml"
fi

# 4. Install systemd service
echo "[4/5] Installing systemd user service..."
mkdir -p "$SYSTEMD_DIR"
cp "$SCRIPT_DIR/attention-tracker.service" "$SYSTEMD_DIR/"
systemctl --user daemon-reload
echo "  Service installed"

# 5. Verify
echo "[5/5] Verifying installation..."
if command -v attention-tracker &>/dev/null; then
    echo "  CLI available: $(which attention-tracker)"
else
    echo "  CLI available via: python -m attention_tracker"
fi
attention-tracker rule validate 2>/dev/null && echo "  Rules valid" || echo "  Rule validation skipped (run manually)"

echo ""
echo "=== Installation complete ==="
echo ""
echo "Quick start:"
echo "  attention-tracker start          # start the daemon"
echo "  attention-tracker status         # check if running"
echo "  attention-tracker today          # see today's summary"
echo ""
echo "Auto-start on login:"
echo "  systemctl --user enable attention-tracker"
echo ""
echo "Morning routine hook:"
echo "  attention-tracker yesterday --oneliner"
echo ""
echo "Decision Journal hook:"
echo "  attention-tracker journal >> ~/shared/context/intake/attention-insight.md"
