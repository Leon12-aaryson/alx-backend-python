#!/bin/bash

# Test Runner Script for Django Messaging App
# This script runs tests locally to validate the setup

echo "🧪 Running Django Messaging App Tests..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the messaging_app directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-django pytest-cov flake8 coverage

echo "🔍 Running code quality checks..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

echo "🧪 Running Django tests..."
python manage.py test chats --verbosity=2

echo "📊 Running tests with coverage..."
pytest --cov=chats --cov-report=html --cov-report=term-missing

echo "✅ Tests completed!"
echo "📁 Coverage report available in: htmlcov/index.html"
echo "🌐 Open htmlcov/index.html in your browser to view coverage report"
