#!/usr/bin/env python3
"""
Simple setup script for the Talishar Data Downloader.

This script helps users get started quickly by:
1. Installing dependencies
2. Setting up the .env file
3. Running a test download
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False


def setup_environment() -> bool:
    """Set up the .env file if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print("✅ .env file already exists")
        return True

    if not env_example.exists():
        print("❌ .env.example file not found")
        return False

    print("📝 Creating .env file from template...")
    try:
        with open(env_example, "r") as f:
            content = f.read()

        with open(env_file, "w") as f:
            f.write(content)

        print("✅ .env file created")
        print("⚠️  Please edit .env and add your API key!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def main() -> None:
    """Main setup function."""
    print("🚀 Setting up Talishar Data Downloader")
    print("=" * 40)

    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)

    print(f"✅ Python {sys.version.split()[0]} detected")

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Setup failed at dependency installation")
        sys.exit(1)

    # Set up environment file
    if not setup_environment():
        print("❌ Setup failed at environment setup")
        sys.exit(1)

    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✅ Data directory ready")

    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env and add your API key")
    print("2. Run: python examples/simple_download.py")
    print("\nFor help, check the README.md file")


if __name__ == "__main__":
    main()
