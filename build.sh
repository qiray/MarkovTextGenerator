#!/bin/bash

RED='\e[1;31m'
GREEN='\e[1;32m'
NC='\e[0m'

echo "Building executable"
# pyinstaller --onefile --windowed main.py -n mathartist --hidden-import=palettes $ADD_BINARY --icon=icon.ico
pyinstaller --onefile main.py -n MarkovTextGenerator --exclude-module matplotlib --exclude-module qt5 --additional-hooks-dir=. || {
    echo -e "${RED}Failed!${NC}"
    exit 1
}
cp README.md dist/
cp LICENSE dist/
echo -e "${GREEN}Done!${NC}"
