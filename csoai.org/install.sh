#!/bin/bash
# SOV3 Open Hands OS — TUI Installer for Mac/Linux/Windows
# Usage: curl -sSL https://raw.githubusercontent.com/CSOAI-ORG/clawd-workspace/main/csoai.org/install.sh | bash
#
# This installs the SOV3 sovereign AI OS stack to ~/.sov3/
# Then you can run `sov3` to launch the TUI.

set -e

# Configurable URLs
GITHUB_RAW="https://raw.githubusercontent.com/CSOAI-ORG/clawd-workspace/main"
# Fallback to local (when running from a Mac clone)
LOCAL_REPO="${SOV3_LOCAL_REPO:-$HOME/clawd}"

echo "🜏 SOV3 Open Hands OS — Installer"
echo ""

# Detect OS
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
  darwin) OS="macos" ;;
  linux) OS="linux" ;;
  mingw*|msys*|cygwin*) OS="windows" ;;
esac
echo "Detected OS: $OS"

# Check Python 3
if ! command -v python3 &> /dev/null; then
  echo "❌ Python 3 not found."
  case "$OS" in
    macos) echo "Install via: brew install python@3.11" ;;
    linux) echo "Install via: sudo apt-get install python3.11 (or your distro's package manager)" ;;
    windows) echo "Install via: https://www.python.org/downloads/" ;;
  esac
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Install path
INSTALL_PATH="$HOME/.sov3"
mkdir -p "$INSTALL_PATH"

# Try GitHub raw first; fall back to local repo
echo "Downloading SOV3 sovereign substrate..."

if [ -d "$LOCAL_REPO" ]; then
  echo "Using local repo: $LOCAL_REPO"
  cp -R "$LOCAL_REPO/sovereign-temple/." "$INSTALL_PATH/" 2>/dev/null || cp -R "$LOCAL_REPO/sovereign-temple/" "$INSTALL_PATH/"
else
  echo "Local repo not found, downloading from GitHub..."
  curl -sSL "$GITHUB_RAW/sovereign-temple.tar.gz" -o /tmp/sov3.tar.gz 2>/dev/null || {
    # Final fallback: clone
    git clone --depth 1 https://github.com/CSOAI-ORG/clawd-workspace.git "$INSTALL_PATH/repo"
  }
fi

# Mark installed
cat > "$INSTALL_PATH/INSTALLED" << EOF
installed_at: $(date)
os: $OS
python: $PYTHON_VERSION
install_method: install.sh
sigil: $(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')
EOF

# Create launcher script
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/sov3" << EOF
#!/bin/bash
# SOV3 sovereign AI OS launcher
INSTALL_PATH="\$HOME/.sov3"
if [ ! -d "\$INSTALL_PATH" ]; then
  echo "❌ SOV3 not installed. Run: curl -sSL $GITHUB_RAW/csoai.org/install.sh | bash"
  exit 1
fi
echo "🜏 SOV3 Open Hands OS — Sovereign AI OS"
echo ""
echo "Install path: \$INSTALL_PATH"
echo "OS: $OS"
echo "Python: $PYTHON_VERSION"
echo "SIGIL: \$(cat \$INSTALL_PATH/INSTALLED 2>/dev/null | grep sigil | cut -d' ' -f2)"
echo ""
echo "Available tools: \$INSTALL_PATH/sovereign-mcp-server.py (276 SOV3 tools)"
echo ""
echo "Launch the TUI:"
echo "  python3 \$INSTALL_PATH/sovereign-mcp-server.py"
echo ""
echo "Or query SOV3 directly:"
echo "  curl -s -m 5 http://localhost:3101/mcp -X POST -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"tools/list\",\"params\":{}}'"
echo ""
echo "🜏 The world is sovereign. Run SOV3 from anywhere."
EOF
chmod +x "$HOME/.local/bin/sov3"

# Try to add to PATH automatically (add to ~/.zshrc or ~/.bashrc)
RC="$HOME/.zshrc"
if [ ! -f "$RC" ]; then
  RC="$HOME/.bashrc"
fi
if [ -f "$RC" ] && ! grep -q '.local/bin' "$RC" 2>/dev/null; then
  echo "" >> "$RC"
  echo '# Added by SOV3 Open Hands installer' >> "$RC"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC"
  echo "Added PATH to $RC"
fi

echo ""
echo "✅ SOV3 Open Hands OS installed successfully!"
echo ""
echo "Launch with: sov3"
echo "Or directly: $HOME/.local/bin/sov3"
echo ""
echo "The sovereign AI OS is yours. The minute you launch, it starts working it out."
echo "🜏 Public install: curl -sSL https://raw.githubusercontent.com/CSOAI-ORG/clawd-workspace/main/csoai.org/install.sh | bash"
echo "🜏 Public URL: csoai.org (when deployed)"