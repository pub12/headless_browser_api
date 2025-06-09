#!/bin/bash

# Setup script for the HTML Fetcher API

echo "Setting up HTML Fetcher API environment..."

# Check for Python 3.7+
python_version=$(python3 --version 2>&1)
if [[ ! $python_version =~ "Python 3" ]]; then
  echo "Error: Python 3 is required."
  exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers (webkit)..."
playwright install webkit

# Create sample .env file if it doesn't exist
if [ ! -f ".env" ]; then
  echo "Creating sample .env file..."
  echo "APPROVED_IPS=127.0.0.1,192.168.1.1,10.0.0.1" > .env
  echo "Sample .env file created. Please edit it with your approved IP addresses."
fi

echo "Setup complete! You can now run the application with:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo "The API will be available at http://localhost:4113" 