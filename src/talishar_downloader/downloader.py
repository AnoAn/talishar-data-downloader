"""
Talishar data downloader module.

This module provides functionality to download Flesh and Blood game data
from the Talishar API in various formats.
"""

import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime, date


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
        "-1": "Clash",
    }

    def __init__(self, api_key: str) -> None:
        """
        Initialize the Talishar downloader.

        Args:
            api_key: Your Talishar API key
        """
        self.api_key = api_key
        self.base_url = "https://fab-insights.azurewebsites.net/api/get_results_blob"

    def get_download_url(
        self, start_date: str, end_date: str, format_code: str = "0"
    ) -> Optional[str]:
        """
        Request a download URL from the Talishar API.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            format_code: Game format code (default: "0" for Classic Constructed)

        Returns:
            Download URL if successful, None if failed
        """
        try:
            response = requests.get(
                self.base_url,
                params={
                    "format": format_code,
                    "start_date": start_date,
                    "end_date": end_date,
                },
                headers={"x-functions-key": self.api_key},
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("download_url")
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            return None

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
                os.makedirs(os.path.dirname(filename), exist_ok=True)

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

    def download_data(
        self,
        start_date: str,
        end_date: str,
        format_code: str = "0",
        output_dir: str = "data",
    ) -> bool:
        """
        Download data for a specific date range and format.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            format_code: Game format code (default: "0" for Classic Constructed)
            output_dir: Directory to save the downloaded file

        Returns:
            True if successful, False if failed
        """
        print(
            f"🔄 Requesting {self.FORMATS.get(format_code, 'Unknown Format')} data for {start_date} to {end_date}..."
        )

        # Get download URL
        download_url = self.get_download_url(start_date, end_date, format_code)

        if not download_url:
            print("❌ Failed to get download URL")
            return False

        # Create filename
        format_name = (
            self.FORMATS.get(format_code, f"format_{format_code}")
            .replace(" ", "_")
            .lower()
        )
        filename = f"{output_dir}/talishar_{format_name}_{start_date}_{end_date}.csv"

        # Download the file
        success = self.download_csv_file(download_url, filename)

        if success:
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
