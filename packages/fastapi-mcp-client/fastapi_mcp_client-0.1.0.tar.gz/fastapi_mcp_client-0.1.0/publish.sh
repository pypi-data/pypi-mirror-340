#!/bin/bash
set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting package publication process...${NC}"

# Check if .pypirc exists, create if not
PYPIRC="$HOME/.pypirc"
if [ ! -f "$PYPIRC" ]; then
    echo -e "${YELLOW}No .pypirc file found. Creating a template at $PYPIRC${NC}"
    cat > "$PYPIRC" << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-test-your-token-here
EOF
    chmod 600 "$PYPIRC"  # Secure the file
    echo -e "${YELLOW}IMPORTANT: Please edit $PYPIRC and add your API tokens before continuing.${NC}"
    echo -e "${YELLOW}You can get your tokens from:${NC}"
    echo -e "${YELLOW}- PyPI: https://pypi.org/manage/account/token/${NC}"
    echo -e "${YELLOW}- TestPyPI: https://test.pypi.org/manage/account/token/${NC}"
    echo -e "${YELLOW}IMPORTANT: Make sure your token starts with 'pypi-' prefix${NC}"
    exit 1
fi

# Clean previous build artifacts
echo -e "${GREEN}Cleaning previous build artifacts...${NC}"
rm -rf dist build

# Ensure build dependencies are installed
echo -e "${GREEN}Ensuring build dependencies are installed...${NC}"
uv add --dev build twine

# Build the package
echo -e "${GREEN}Building the package...${NC}"
uv run -m build

# Show files to be uploaded
echo -e "${GREEN}Files to be uploaded:${NC}"
ls -l dist/

# Ask if upload to test PyPI first
read -p "Upload to Test PyPI first? (y/n) " test_first
if [ "$test_first" = "y" ] || [ "$test_first" = "Y" ]; then
    echo -e "${GREEN}Uploading to Test PyPI...${NC}"
    
    # Ask for TestPyPI token directly
    echo -e "${YELLOW}Enter your TestPyPI token (starts with 'pypi-'):${NC}"
    read -s TEST_PYPI_TOKEN
    
    # Check if token was provided, fall back to .pypirc if empty
    if [ -z "$TEST_PYPI_TOKEN" ]; then
        echo -e "${YELLOW}No token provided, trying to use .pypirc...${NC}"
        uv run -m twine upload --verbose \
          --repository-url https://test.pypi.org/legacy/ dist/*
    else
        # Use the provided token directly
        TWINE_USERNAME="__token__" TWINE_PASSWORD="$TEST_PYPI_TOKEN" \
        uv run -m twine upload --verbose \
          --repository-url https://test.pypi.org/legacy/ dist/*
    fi
    
    # Check upload status
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Test PyPI upload successful!${NC}"
        echo -e "${GREEN}You can test installation with:${NC}"
        echo -e "${GREEN}uv add --index-url https://test.pypi.org/simple/ fastapi-mcp-client${NC}"
    else
        echo -e "${RED}Test PyPI upload failed!${NC}"
        echo -e "${YELLOW}Common issues:${NC}"
        echo -e "${YELLOW}1. Token may be incorrect or not have proper permissions${NC}"
        echo -e "${YELLOW}2. Token must start with 'pypi-' prefix${NC}"
        echo -e "${YELLOW}3. Package name might already be taken on TestPyPI${NC}"
        echo -e "${YELLOW}Visit https://test.pypi.org/help/#invalid-auth for more information.${NC}"
        exit 1
    fi
    
    # Ask to proceed with real PyPI upload
    read -p "Proceed with uploading to PyPI? (y/n) " proceed
    if [ "$proceed" != "y" ] && [ "$proceed" != "Y" ]; then
        echo -e "${YELLOW}Upload to PyPI aborted.${NC}"
        exit 0
    fi
fi

# Upload to PyPI
echo -e "${GREEN}Uploading to PyPI...${NC}"

# Ask for PyPI token directly
echo -e "${YELLOW}Enter your PyPI token (starts with 'pypi-'):${NC}"
read -s PYPI_TOKEN

# Check if token was provided, fall back to .pypirc if empty
if [ -z "$PYPI_TOKEN" ]; then
    echo -e "${YELLOW}No token provided, trying to use .pypirc...${NC}"
    uv run -m twine upload --verbose dist/*
else
    # Use the provided token directly
    TWINE_USERNAME="__token__" TWINE_PASSWORD="$PYPI_TOKEN" \
    uv run -m twine upload --verbose dist/*
fi

# Check upload status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}PyPI upload successful!${NC}"
    echo -e "${GREEN}Your package can now be installed with:${NC}"
    echo -e "${GREEN}uv add fastapi-mcp-client${NC}"
else
    echo -e "${RED}PyPI upload failed!${NC}"
    echo -e "${YELLOW}Common issues:${NC}"
    echo -e "${YELLOW}1. Token may be incorrect or not have proper permissions${NC}"
    echo -e "${YELLOW}2. Token must start with 'pypi-' prefix${NC}"
    echo -e "${YELLOW}3. Package name might already be taken on PyPI${NC}"
    echo -e "${YELLOW}Visit https://pypi.org/help/#invalid-auth for more information.${NC}"
    exit 1
fi

echo -e "${GREEN}Publication process completed!${NC}"