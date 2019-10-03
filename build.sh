#!/bin/bash

RED='\e[1;31m'
GREEN='\e[1;32m'
NC='\e[0m'

echo "Building executable"
pyinstaller --onefile main.py -n MarkovTextGenerator || {
    echo -e "${RED}Failed!${NC}"
    exit 1
}
cp README.md dist/
cp LICENSE dist/
echo -e "${GREEN}Done!${NC}"
