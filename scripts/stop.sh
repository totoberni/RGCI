#!/bin/bash
# Script to stop and remove RGCI environment

# Define colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Cleaning up RGCI environment...${NC}"

# Check if venv exists
if [ -d "venv" ]; then
    # Deactivate virtual environment if active
    if [[ "$VIRTUAL_ENV" == *"venv"* ]]; then
        echo -e "${YELLOW}Deactivating virtual environment...${NC}"
        deactivate 2>/dev/null
    fi
    
    # Remove virtual environment
    echo -e "${YELLOW}Removing virtual environment...${NC}"
    rm -rf venv
else
    echo -e "${YELLOW}No virtual environment found.${NC}"
fi

# Clean pip cache
echo -e "${YELLOW}Cleaning pip cache...${NC}"
pip cache purge 2>/dev/null || echo -e "${YELLOW}Failed to clean pip cache. May require manual deletion.${NC}"

echo -e "${GREEN}Environment cleanup complete!${NC}"
echo -e "${YELLOW}Note: The .env file in config directory was not removed. Delete it manually if needed.${NC}" 