#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[+]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }

# ── Python venv ──
if [ ! -d "$VENV_DIR" ]; then
    log "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    log "Virtual environment exists"
fi

source "$VENV_DIR/bin/activate"

# ── Pip dependencies ──
log "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r "$SCRIPT_DIR/requirements.txt"
log "Pip packages installed"

# ── Docker ──
if ! command -v docker &> /dev/null; then
    warn "Docker not found. Please install Docker first."
fi

# ── Clone Camofox repo if not present ──
if [ ! -d "$SCRIPT_DIR/camofox-browser" ]; then
    log "Cloning Camofox browser repo..."
    git clone https://github.com/jo-inc/camofox-browser.git "$SCRIPT_DIR/camofox-browser"
fi

# ── Build Docker image (if not already built) ──
if sudo docker images camofox-browser --format "{{.Repository}}" 2>/dev/null | grep -q "^camofox-browser$"; then
    log "Camofox Docker image already exists"
else
    log "Building Camofox Docker image (requires sudo, ~1.8GB)..."
    cd "$SCRIPT_DIR/camofox-browser"
    sudo docker build --no-cache -t camofox-browser .
    log "Camofox image built"
fi

# ── Data directories ──
mkdir -p "$SCRIPT_DIR/data"
mkdir -p "$SCRIPT_DIR/data/logs"

# ── Config check ──
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    warn ".env not found — copying from .env.example"
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
fi

log "Setup complete. Run ./start.sh to start the service."
