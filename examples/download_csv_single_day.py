#!/usr/bin/env python3
"""
Example script to download Talishar data for a single day using the new CSV endpoint.

This script uses the new /download_csv endpoint which provides pre-generated CSV files
for a single day. This is the recommended approach going forward.

Just change the date and format below!
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

# Add the parent directory to the path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.talishar_downloader import TalisharDownloader


def download_csv_single_day(
    api_key: str, date: str, format_code: str = "0", output_dir: str = "data"
) -> bool:
    """
    Download CSV file for a single day using the new /download_csv endpoint.

    Args:
        api_key: Your API key
        date: Date in YYYY-MM-DD format (e.g., "2025-09-02")
        format_code: Game format identifier (default: "0" for Classic Constructed)
        output_dir: Directory to save the downloaded file

    Returns:
        True if successful, False if failed
    """
    base_url = "https://fab-insights.azurewebsites.net/api/v1/download_csv"

    print(
        f"🔄 Requesting CSV for {TalisharDownloader.FORMATS.get(format_code, 'Unknown Format')} on {date}..."
    )

    try:
        # Step 1: Get download URL from the new endpoint
        response = requests.get(
            base_url,
            params={"format": format_code, "date": date},
            headers={"x-functions-key": api_key},
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            download_url = data.get("download_url")

            if not download_url:
                print("❌ No download URL in response")
                return False

            # Extract metadata from response
            blob_name = data.get("blob_name", "unknown")
            expires_at = data.get("expires_at", "unknown")
            print(f"✅ Download URL received (expires at: {expires_at})")

            # Step 2: Download the CSV file
            csv_response = requests.get(download_url, timeout=60)

            if csv_response.status_code == 200:
                # Create output directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)

                # Create filename from blob name or date/format
                if blob_name and blob_name.endswith(".csv"):
                    filename = os.path.join(output_dir, blob_name)
                else:
                    format_name = (
                        TalisharDownloader.FORMATS.get(
                            format_code, f"format_{format_code}"
                        )
                        .replace(" ", "_")
                        .lower()
                    )
                    filename = os.path.join(
                        output_dir, f"talishar_{format_name}_{date}.csv"
                    )

                with open(filename, "wb") as f:
                    f.write(csv_response.content)

                print(f"✅ Successfully downloaded: {filename}")
                print(f"📁 File saved to: {filename}")
                return True
            else:
                print(f"❌ Download Error: {csv_response.status_code}")
                print(f"Response: {csv_response.text}")
                return False

        elif response.status_code == 404:
            print(f"❌ CSV file not found for format {format_code} and date {date}")
            print("   Make sure the date is valid and data exists for that date")
            return False
        elif response.status_code == 400:
            print(f"❌ Invalid parameters: {response.text}")
            return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except IOError as e:
        print(f"❌ File writing error: {e}")
        return False


def main() -> None:
    """Download Talishar data for a single day with simple configuration."""
    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment variable
    api_key = os.getenv("FUNCTION_API_KEY")
    if not api_key:
        print("❌ Error: Please set your FUNCTION_API_KEY in a .env file")
        print("   Create a .env file with: FUNCTION_API_KEY=your_api_key_here")
        return

    # ===== CONFIGURATION - MODIFY THESE VALUES =====
    DATE = "2025-09-02"  # Change this to your desired date (data available from November 2025 onwards)
    FORMAT_CODE = "0"  # Change this to your desired format (see list below)
    OUTPUT_DIR = "data"  # Directory to save the downloaded file
    # ===============================================

    # Show available formats
    print("Available formats:")
    downloader = TalisharDownloader(api_key)
    downloader.list_formats()
    print()

    # Download the data
    success = download_csv_single_day(
        api_key=api_key, date=DATE, format_code=FORMAT_CODE, output_dir=OUTPUT_DIR
    )

    if success:
        print("🎉 All done! Check your data folder for the downloaded file.")
    else:
        print("❌ Download failed. Please check your API key and try again.")


if __name__ == "__main__":
    main()
