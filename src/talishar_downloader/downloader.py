"""
Talishar data downloader module.

This module provides functionality to download Flesh and Blood game data
from the Talishar API in various formats.
"""

import os
import requests
from typing import Optional, Dict, Any


class TalisharDownloader:
    """
    A simple class to download Flesh and Blood game data from Talishar API.

    This class handles API authentication, data requests, and file downloads
    for various game formats.
    """

    # Format mapping for easy reference
    FORMATS = {
        "0": "Classic Constructed (CC)",
        "1": "Competitive CC",
        "2": "Blitz",
        "3": "Competitive Blitz",
        "4": "Open Format CC",
        "5": "Commoner",
        "6": "Sealed",
        "7": "Draft",
        "8": "Living Legend CC",
        "9": "Living Legend Blitz",
        "10": "Open Format Blitz",
        "11": "Open Format Living Legend CC",
        "12": "Open Format Living Legend Blitz",
        "13": "Competitive LL",
        "14": "Silver Age",
        "15": "Competitive Silver Age",
        "-1": "Clash",
    }

    def __init__(self, api_key: str) -> None:
        """
        Initialize the Talishar downloader.

        Args:
            api_key: Your Talishar API key
        """
        self.api_key = api_key
        self.base_url_csv = "https://fab-insights.azurewebsites.net/api/v1/download_csv"

    def download_csv_file(self, download_url: str, filename: str) -> bool:
        """
        Download CSV file from the provided URL.

        Args:
            download_url: URL to download the CSV from
            filename: Name to save the file as

        Returns:
            True if successful, False if failed
        """
        try:
            response = requests.get(download_url, timeout=60)

            if response.status_code == 200:
                # Create directory if it doesn't exist
                dirname = os.path.dirname(filename)
                if dirname:
                    os.makedirs(dirname, exist_ok=True)

                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"✅ Successfully downloaded: {filename}")
                return True
            else:
                print(f"❌ Download Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        except requests.RequestException as e:
            print(f"❌ Download error: {e}")
            return False
        except IOError as e:
            print(f"❌ File writing error: {e}")
            return False

    def get_csv_download_url(
        self, date: Optional[str] = None, format_code: str = "0"
    ) -> Optional[Dict[str, Any]]:
        """
        Request a download URL from the CSV endpoint for a single day.

        This method uses the /v1/download_csv endpoint which provides
        pre-generated CSV files for a single day.

        Args:
            date: Date in YYYY-MM-DD format (e.g., "2025-09-02").
                  If not provided, returns the latest available date for the format.
            format_code: Game format code (default: "0" for Classic Constructed)

        Returns:
            Dictionary containing download_url, expires_at, blob_name, format, date, version
            if successful, None if failed
        """
        try:
            params: Dict[str, str] = {"format": format_code}
            if date:
                params["date"] = date

            response = requests.get(
                self.base_url_csv,
                params=params,
                headers={"x-functions-key": self.api_key},
                timeout=30,
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(
                    f"❌ CSV file not found for format {format_code}"
                    + (f" and date {date}" if date else "")
                )
                print("   Make sure the date is valid and data exists for that date")
                return None
            elif response.status_code == 400:
                print(f"❌ Invalid parameters: {response.text}")
                return None
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return None

    def download_csv_single_day(
        self,
        date: Optional[str] = None,
        format_code: str = "0",
        output_dir: str = "data",
    ) -> bool:
        """
        Download CSV file for a single day using the /download_csv endpoint.

        This method uses pre-generated CSV files which are faster and more efficient.

        Args:
            date: Date in YYYY-MM-DD format (e.g., "2025-09-02").
                  If not provided, downloads the latest available date for the format.
            format_code: Game format code (default: "0" for Classic Constructed)
            output_dir: Directory to save the downloaded file

        Returns:
            True if successful, False if failed
        """
        date_str = date if date else "latest"
        print(
            f"🔄 Requesting {self.FORMATS.get(format_code, 'Unknown Format')} CSV for {date_str}..."
        )

        # Get download URL and metadata from endpoint
        response_data = self.get_csv_download_url(date, format_code)

        if not response_data:
            print("❌ Failed to get download URL")
            return False

        download_url = response_data.get("download_url")
        if not download_url:
            print("❌ No download URL in response")
            return False

        # Use blob_name from response if available, otherwise generate filename
        blob_name = response_data.get("blob_name")
        actual_date = response_data.get("date", date_str)

        if blob_name and blob_name.endswith(".csv"):
            filename = os.path.join(output_dir, blob_name)
        else:
            format_name = (
                self.FORMATS.get(format_code, f"format_{format_code}")
                .replace(" ", "_")
                .lower()
            )
            filename = os.path.join(
                output_dir, f"talishar_{format_name}_{actual_date}.csv"
            )

        # Download the file
        success = self.download_csv_file(download_url, filename)

        if success:
            expires_at = response_data.get("expires_at", "unknown")
            print(f"✅ Download URL expires at: {expires_at}")
            print(f"🎉 Download completed successfully!")
            print(f"📁 File saved to: {filename}")

        return success

    def list_formats(self) -> None:
        """Print all available game formats."""
        print("📋 Available Game Formats:")
        print("-" * 40)
        for code, name in self.FORMATS.items():
            print(f"  {code:>3}: {name}")
        print("-" * 40)
