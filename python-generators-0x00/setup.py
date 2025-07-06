#!/usr/bin/env python3
"""
Setup script for the Python Generators MySQL Database Streaming project.
This script helps users configure their environment and test the setup.
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is suitable."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not supported")
        print("  Please use Python 3.6 or higher")
        return False

def install_requirements():
    """Install required packages."""
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'mysql-connector-python'])
        print("✓ mysql-connector-python installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install mysql-connector-python")
        print("  Please install it manually: pip install mysql-connector-python")
        return False

def check_mysql_connection():
    """Check if MySQL connection can be established."""
    print("\nChecking MySQL connection...")
    try:
        import mysql.connector
        # Try to connect (this will likely fail without proper credentials)
        # but at least we can check if the module loads
        print("✓ mysql-connector-python module loaded successfully")
        print("  Note: Actual database connection will be tested when you run the scripts")
        return True
    except ImportError:
        print("✗ mysql-connector-python module not found")
        return False

def create_sample_config():
    """Create a sample configuration file."""
    print("\nCreating sample configuration...")
    config_content = """# Database Configuration
# Update these values according to your MySQL setup

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password_here',  # Change this!
    'database': 'ALX_prodev'
}

# Usage:
# from config import DATABASE_CONFIG
# connection = mysql.connector.connect(**DATABASE_CONFIG)
"""
    
    try:
        with open('config.py', 'w') as f:
            f.write(config_content)
        print("✓ Sample configuration file created: config.py")
        print("  Please update the database credentials in config.py")
        return True
    except Exception as e:
        print(f"✗ Failed to create config.py: {e}")
        return False

def main():
    """Main setup function."""
    print("Python Generators MySQL Database Streaming - Setup")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Check MySQL connection
    if not check_mysql_connection():
        success = False
    
    # Create sample config
    if not create_sample_config():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Update database credentials in config.py")
        print("2. Make sure MySQL server is running")
        print("3. Run: python3 seed.py to set up the database")
        print("4. Run: python3 0-main.py to test the setup")
        print("5. Run: python3 example_usage.py to see the generator in action")
    else:
        print("✗ Setup completed with errors")
        print("Please address the issues above before proceeding")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
