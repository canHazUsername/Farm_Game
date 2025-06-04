#!/bin/bash

# Fail immediately if any command errors
set -e

# Clean previous build artifacts
rm -rf build dist *.spec

# Run PyInstaller build
pyinstaller --onefile --windowed \
  --add-data "assets:assets" \
  --add-data "sav:sav" \
  game.py

echo ""
echo "Build complete."
echo "Output binary: dist/game"
