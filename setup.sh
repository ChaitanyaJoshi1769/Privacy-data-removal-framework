#!/bin/bash
# Privacy Data Removal Framework - Automated Setup

set -e

echo "=========================================="
echo "Privacy Data Removal Framework - Setup"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python3 --version

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create necessary directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p logs data config
echo -e "${GREEN}✓ Directories created${NC}"

# Copy config template if needed
if [ ! -f "scripts/config.json" ] && [ -f "scripts/config.example.json" ]; then
    echo -e "${BLUE}Copying configuration template...${NC}"
    cp scripts/config.example.json scripts/config.json
    echo -e "${YELLOW}⚠ Edit scripts/config.json with your details${NC}"
fi

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cat > .env << 'ENVEOF'
REMOVAL_NAME=Your Name
REMOVAL_EMAIL=your.email@example.com
REMOVAL_PHONE=555-555-5555
ENVEOF
    echo -e "${YELLOW}⚠ Edit .env file with your information${NC}"
fi

echo ""
echo -e "${GREEN}Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env with your identity"
echo "2. Run: python3 scripts/main.py --full"
echo ""
