#!/bin/bash
# Setup script for RGCI environment

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up RGCI environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Please check your Python installation."
    exit 1
fi

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo -e "${YELLOW}Creating .env file from example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please update the .env file with your API keys.${NC}"
fi

echo -e "${GREEN}Environment setup complete!${NC}"
echo -e "${GREEN}Virtual environment is active. Run 'deactivate' to exit.${NC}"
echo -e "${YELLOW}Usage examples:${NC}"
echo -e "  - Generate test data: python scripts/run_data_gen.py <settings_index>"
echo -e "  - Run evaluation: python scripts/run_evaluation.py <settings_index>" 