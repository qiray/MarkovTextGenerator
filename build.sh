#!/bin/bash

RED='\e[1;31m'
GREEN='\e[1;32m'
NC='\e[0m'

echo "Building executable"
pyinstaller main.py -n MarkovTextGenerator --onefile --exclude-module matplotlib --exclude-module qt5 --clean --additional-hooks-dir=. || {
    echo -e "${RED}Failed!${NC}"
    exit 1
}
cp README.md dist/
cp LICENSE dist/
echo -e "${GREEN}Done!${NC}"
