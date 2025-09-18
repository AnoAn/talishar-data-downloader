#!/usr/bin/env python3
"""
Simple example script to download Talishar data.

This is a basic example that users can copy and modify for their needs.
Just change the dates, format, and API key below!
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.talishar_downloader import TalisharDownloader


def main() -> None:
    """Download Talishar data with simple configuration."""
    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment variable
    api_key = os.getenv("FUNCTION_API_KEY")
    if not api_key:
        print("❌ Error: Please set your FUNCTION_API_KEY in a .env file")
        print("   Create a .env file with: FUNCTION_API_KEY=your_api_key_here")
        return

    # Create downloader instance
    downloader = TalisharDownloader(api_key)

    # ===== CONFIGURATION - MODIFY THESE VALUES =====
    START_DATE = "2025-09-02"  # Change this to your desired start date
    END_DATE = "2025-09-03"  # Change this to your desired end date
    FORMAT_CODE = "0"  # Change this to your desired format (see list below)
    OUTPUT_DIR = "data"  # Directory to save the downloaded file
    # ===============================================

    # Show available formats
    print("Available formats:")
    downloader.list_formats()
    print()

    # Download the data
    success = downloader.download_data(
        start_date=START_DATE,
        end_date=END_DATE,
        format_code=FORMAT_CODE,
        output_dir=OUTPUT_DIR,
    )

    if success:
        print("🎉 All done! Check your data folder for the downloaded file.")
    else:
        print("❌ Download failed. Please check your API key and try again.")


if __name__ == "__main__":
    main()
