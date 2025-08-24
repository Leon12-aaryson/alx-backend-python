#!/bin/bash

# Validation Script for Jenkins and GitHub Actions Setup
# This script validates that all required components are in place

echo "🔍 Validating Jenkins and GitHub Actions Setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 (MISSING)${NC}"
        return 1
    fi
}

# Function to check if directory exists
check_directory() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 (MISSING)${NC}"
        return 1
    fi
}

# Function to check if file is executable
check_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✅ $1 (executable)${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  $1 (not executable)${NC}"
        return 1
    fi
}

echo ""
echo "📁 Checking required files and directories..."
echo "=============================================="

# Check core files
check_file "Jenkinsfile"
check_file "pytest.ini"
check_file ".flake8"
check_file "requirements.txt"
check_file "Dockerfile"
check_file "manage.py"

# Check GitHub Actions workflows
check_directory ".github/workflows"
check_file ".github/workflows/ci.yml"
check_file ".github/workflows/dep.yml"

# Check test files
check_file "chats/tests.py"
check_file "chats/models.py"
check_file "chats/views.py"

# Check setup scripts
check_executable "setup_jenkins.sh"
check_executable "run_tests.sh"
check_executable "validate_setup.sh"

# Check documentation
check_file "JENKINS_SETUP.md"
check_file "SETUP_SUMMARY.md"

echo ""
echo "🔧 Checking Docker setup..."
echo "=========================="

# Check if Docker is running
if docker info > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker is running${NC}"
else
    echo -e "${RED}❌ Docker is not running${NC}"
fi

# Check if Jenkins container exists
if docker ps -a --format 'table {{.Names}}' | grep -q "jenkins"; then
    echo -e "${GREEN}✅ Jenkins container exists${NC}"
    
    # Check if it's running
    if docker ps --format 'table {{.Names}}' | grep -q "jenkins"; then
        echo -e "${GREEN}✅ Jenkins container is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Jenkins container exists but is not running${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Jenkins container does not exist${NC}"
fi

echo ""
echo "🐍 Checking Python environment..."
echo "================================"

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 not found${NC}"
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 is available${NC}"
else
    echo -e "${YELLOW}⚠️  pip3 not found${NC}"
fi

echo ""
echo "📊 Summary..."
echo "============="

# Count total checks
TOTAL_CHECKS=0
PASSED_CHECKS=0

# Function to count checks
count_check() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ $? -eq 0 ]; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    fi
}

# Re-run checks to count
check_file "Jenkinsfile" > /dev/null; count_check
check_file "pytest.ini" > /dev/null; count_check
check_file ".flake8" > /dev/null; count_check
check_file "requirements.txt" > /dev/null; count_check
check_file "Dockerfile" > /dev/null; count_check
check_file "manage.py" > /dev/null; count_check
check_directory ".github/workflows" > /dev/null; count_check
check_file ".github/workflows/ci.yml" > /dev/null; count_check
check_file ".github/workflows/dep.yml" > /dev/null; count_check
check_file "chats/tests.py" > /dev/null; count_check
check_executable "setup_jenkins.sh" > /dev/null; count_check
check_executable "run_tests.sh" > /dev/null; count_check

echo ""
echo -e "${GREEN}✅ Setup Validation Complete!${NC}"
echo "====================================="
echo -e "Passed: ${GREEN}$PASSED_CHECKS${NC} / $TOTAL_CHECKS checks"
echo ""

if [ $PASSED_CHECKS -eq $TOTAL_CHECKS ]; then
    echo -e "${GREEN}🎉 All checks passed! Your setup is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./setup_jenkins.sh"
    echo "2. Access Jenkins at: http://localhost:8080"
    echo "3. Configure credentials and pipeline"
    echo "4. Test with: ./run_tests.sh"
else
    echo -e "${YELLOW}⚠️  Some checks failed. Please review the issues above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "- Ensure you're in the messaging_app directory"
    echo "- Check file permissions: chmod +x *.sh"
    echo "- Verify all files were created properly"
fi

echo ""
