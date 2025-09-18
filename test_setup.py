#!/usr/bin/env python3
"""
Test script to verify the Talishar Data Downloader setup.

This script checks if everything is working correctly.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path so we can import our module
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from talishar_downloader import TalisharDownloader

    print("✅ Module import successful")
except ImportError as e:
    print(f"❌ Module import failed: {e}")
    sys.exit(1)


def test_environment() -> bool:
    """Test if environment is set up correctly."""
    print("🔄 Testing environment setup...")

    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        return False

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("FUNCTION_API_KEY")

    if not api_key:
        print("❌ FUNCTION_API_KEY not found in .env file")
        print("   Please add your API key to the .env file")
        return False

    if api_key == "your_api_key_here":
        print("❌ Please replace the placeholder API key in .env file")
        return False

    print("✅ Environment setup looks good")
    return True


def test_downloader_creation() -> bool:
    """Test if we can create a downloader instance."""
    print("🔄 Testing downloader creation...")

    try:
        load_dotenv()
        api_key = os.getenv("FUNCTION_API_KEY")

        if not api_key or api_key == "your_api_key_here":
            print("⚠️  Skipping downloader test (no valid API key)")
            return True

        downloader = TalisharDownloader(api_key)
        print("✅ Downloader created successfully")

        # Test format listing
        print("🔄 Testing format listing...")
        downloader.list_formats()
        print("✅ Format listing works")

        return True
    except Exception as e:
        print(f"❌ Downloader creation failed: {e}")
        return False


def test_dependencies() -> bool:
    """Test if all dependencies are available."""
    print("🔄 Testing dependencies...")

    try:
        import requests

        print("✅ requests module available")
    except ImportError:
        print("❌ requests module not found")
        print("   Run: pip install -r requirements.txt")
        return False

    try:
        from dotenv import load_dotenv

        print("✅ python-dotenv module available")
    except ImportError:
        print("❌ python-dotenv module not found")
        print("   Run: pip install -r requirements.txt")
        return False

    return True


def main() -> None:
    """Run all tests."""
    print("🧪 Testing Talishar Data Downloader Setup")
    print("=" * 40)

    all_passed = True

    # Test dependencies
    if not test_dependencies():
        all_passed = False

    # Test environment
    if not test_environment():
        all_passed = False

    # Test downloader creation
    if not test_downloader_creation():
        all_passed = False

    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! You're ready to download data.")
        print("\nNext steps:")
        print("1. Make sure your API key is correct in .env")
        print("2. Run: python examples/simple_download.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nFor help, check the README.md file")


if __name__ == "__main__":
    main()
