# FaB Insights Talishar Data Downloader

A **community-supported** Python tool to download public Flesh and Blood game data from [Talishar](https://talishar.net).

> **No data is sold.** This project runs on **voluntary cost-sharing** via [Metafy](https://metafy.gg/@fabinsights) — to cover the server costs (Azure for the API + Hetzner for hosting the database).  
> Every supporter keeps the data flowing for the entire FaB community.

> **📅 Data Availability:** The database contains game data from **June 2025** onwards. Make sure to use dates from June 2025 or later when requesting data.

---

## 🚀 Quick Start (4 Steps)

### 1. Reach out via Metafy
Support the project and get your **personal API key**:
👉 [**Join on Metafy →**](https://metafy.gg/@fabinsights)

Fill this quick form **after joining** to help me keep track where the keys are going:
[Submit Email, Username, purpose →](https://forms.gle/dPkc5iUeiS8DzL4W8)


### 2. Set Up the Project
```bash
# Download this repository
git clone https://github.com/yourusername/fab-talishar-data-download.git
cd fab-talishar-data-download

# Install Python dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your API key
```

### 3. Choose Your Format and Date
Open `examples/download_csv_single_day.py` and modify these lines:
```python
DATE = "2025-09-02"  # Your date (data available from June 2025)
FORMAT_CODE = "0"    # Game format (see table below)
```

### 4. Download Data
```bash
# Run the new example (recommended)
python examples/download_csv_single_day.py

# Or use the legacy date range example
python examples/simple_download.py
```

That's it! Your data will be saved in the `data/` folder.


## 📁 What's Included

```
fab-talishar-data-download/
├── examples/
│   ├── download_csv_single_day.py  # 👈 NEW! Recommended - Single day CSV downloads
│   ├── simple_download.py          # Legacy - Date range downloads
├── src/
│   └── talishar_downloader/    # The main code (you don't need to touch this)
├── data/                       # Your downloaded files go here
├── .env.example               # Template for your API key
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🆕 New API Endpoint (Recommended)

> **We're moving to a new API!** The new `/download_csv` endpoint provides pre-generated CSV files for single-day downloads. This is faster and more efficient. The legacy API (`/get_results_blob`) is still available but we recommend migrating to the new endpoint.

### New API: `/v1/download_csv`

The new endpoint provides pre-generated CSV files for a single day. It accepts:
- `format` (optional): Game format identifier (e.g., "0", "1", "2"). Defaults to "0"
- `date` (optional): Date in YYYY-MM-DD format (e.g., "2025-09-02"). If not provided, returns the latest available date for the format

**Response includes:**
- `download_url`: Temporary SAS URL for downloading the CSV file
- `expires_at`: ISO 8601 timestamp when the URL expires
- `blob_name`: Name of the blob file
- `format`: Game format identifier
- `date`: Requested or latest available date
- `version`: API version

> **📅 Current Day Updates:** For the current day only, data is updated hourly. If you query the same date multiple times throughout the day, the file will be updated with new data until midnight. After midnight, the data for that date becomes final and will no longer be updated.

**Quick Start with New API:**

```bash
# Use the new example script
python examples/download_csv_single_day.py
```

Or modify the script:
```python
DATE = "2025-09-02"  # Single date
FORMAT_CODE = "0"    # Format code
```

**Direct API Call Example:**

```python
import requests

api_key = "YOUR_API_KEY"
response = requests.get(
    "https://fab-insights.azurewebsites.net/api/v1/download_csv",
    params={"format": "0", "date": "2025-09-02"},
    headers={"x-functions-key": api_key}
)

if response.status_code == 200:
    data = response.json()
    download_url = data["download_url"]
    
    # Download the CSV
    csv_response = requests.get(download_url)
    with open("talishar_data.csv", "wb") as f:
        f.write(csv_response.content)
```

**cURL Example:**

```bash
# Get download URL
curl -X GET "https://fab-insights.azurewebsites.net/api/v1/download_csv?format=0&date=2025-09-02" \
     -H "x-functions-key: YOUR_API_KEY" \
     --output response.json

# Extract and download CSV
DOWNLOAD_URL=$(cat response.json | grep -o '"download_url":"[^"]*"' | cut -d'"' -f4)
curl -X GET "$DOWNLOAD_URL" --output talishar_data.csv
```

## 🎮 Game Formats

Choose any format you want:

| Code | Format Name |
|------|---------|
| "0" | Classic Constructed (CC) |
| "1" | Competitive CC |
| "2" | Blitz |
| "3" | Competitive Blitz |
| "4" | Open Format CC |
| "5" | Commoner |
| "6" | Sealed |
| "7" | Draft |
| "8" | Living Legend CC |
| "9" | Living Legend Blitz |
| "10" | Open Format Blitz |
| "11" | Open Format Living Legend CC |
| "12" | Open Format Living Legend Blitz |
| "13" | Competitive LL |
| "14" | Silver Age |
| "15" | Competitive Silver Age |
| "16" | Open Silver Age |
| "-1" | Clash |

## 📝 How to Use

### Option 1: New API - Single Day CSV (Recommended)

1. Open `examples/download_csv_single_day.py`
2. Change these lines to what you want:
   ```python
   DATE = "2025-09-02"  # Single date (data available from June 2025)
   FORMAT_CODE = "0"    # Format code (see table above)
   ```
   _Note:_ Downloads pre-generated CSV for a single day. If date is not provided, returns the latest available date for the format.

3. Run: `python examples/download_csv_single_day.py`

### Option 2: Use the New API in Your Own Script

```python
import requests
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.getenv("FUNCTION_API_KEY")

# Get download URL from new endpoint
response = requests.get(
    "https://fab-insights.azurewebsites.net/api/v1/download_csv",
    params={"format": "0", "date": "2025-11-20"},
    headers={"x-functions-key": api_key}
)

if response.status_code == 200:
    data = response.json()
    download_url = data["download_url"]
    
    # Download the CSV
    csv_response = requests.get(download_url)
    with open("talishar_data.csv", "wb") as f:
        f.write(csv_response.content)
    print("Download complete!")
```

### Option 3: Legacy API - Date Range Downloads

> **Note:** The legacy API is still available but we recommend using the new `/download_csv` endpoint for single-day downloads. The legacy API is useful if you need date ranges.

1. Open `examples/simple_download.py`
2. Change these lines to what you want:
   ```python
   START_DATE = "2025-06-05"  # Your start date (data available from June 2025)
   END_DATE = "2025-06-08"    # Your end date  
   FORMAT_CODE = "0"          # Format code (see table above)
   ```
   _Note:_ max 3 days per call. Data is available from June 2025 onwards.

3. Run: `python examples/simple_download.py`

Or use the Python library:

```python
from src.talishar_downloader import TalisharDownloader
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.getenv("FUNCTION_API_KEY")

# Create downloader
downloader = TalisharDownloader(api_key)

# Download data
success = downloader.download_data(
    start_date="2025-06-05",
    end_date="2025-06-08", 
    format_code="0",  # Classic Constructed
    output_dir="my_data"
)

if success:
    print("Download complete!")
```

---

## 🔄 Legacy API Documentation

> **Legacy API:** The `/get_results_blob` endpoint is still available but we're moving to the new `/download_csv` endpoint. This section is preserved for reference.

### Legacy API: `/get_results_blob`

The legacy endpoint supports date range queries. It accepts:
- `format`: Game format identifier (e.g., "0", "1", "2")
- `start_date`: Start date in YYYY-MM-DD format
- `end_date`: End date in YYYY-MM-DD format (max 3 days per call)
- `days`: Alternative to date range - number of days back from today

#### Legacy cURL Examples

**Download Classic Constructed data for a date range:**
```bash
# Step 1: Get download URL
curl -X GET "https://fab-insights.azurewebsites.net/api/get_results_blob?format=0&start_date=2025-06-05&end_date=2025-06-08" \
     -H "x-functions-key: YOUR_API_KEY" \
     --output response.json

# Step 2: Extract download URL from response and download CSV
DOWNLOAD_URL=$(cat response.json | grep -o '"download_url":"[^"]*"' | cut -d'"' -f4)
curl -X GET "$DOWNLOAD_URL" --output talishar_data.csv
```

**Download Blitz data for last 3 days:**
```bash
curl -X GET "https://fab-insights.azurewebsites.net/api/get_results_blob?format=2&days=3" \
     -H "x-functions-key: YOUR_API_KEY" \
     --output response.json
```

#### Legacy Python requests Example

```python
import requests

# Your API key
api_key = "YOUR_API_KEY"

# Step 1: Get download URL
response = requests.get(
    "https://fab-insights.azurewebsites.net/api/get_results_blob",
    params={
        "format": "0",  # Classic Constructed
        "start_date": "2025-06-05",
        "end_date": "2025-06-08"
    },
    headers={"x-functions-key": api_key}
)

if response.status_code == 200:
    data = response.json()
    download_url = data["download_url"]
    
    # Step 2: Download CSV
    csv_response = requests.get(download_url)
    
    if csv_response.status_code == 200:
        with open("talishar_data.csv", "wb") as f:
            f.write(csv_response.content)
        print("Data downloaded successfully!")
    else:
        print("Failed to download CSV")
else:
    print(f"API Error: {response.status_code}")
```

## 📊 What Data Do You Get?

Each CSV file contains:
- `game_id`: Unique game identifier
- `format`: Game format code
- `deck1_json`: First player's deck (JSON)
- `deck2_json`: Second player's deck (JSON) 
- `player1_name`: First player's name (hashed)
- `player2_name`: Second player's name (hashed)
- `created_at`: When the game was played
- `deck1_id_hash`: Hashed deck ID
- `deck2_id_hash`: Hashed deck ID

### Example of a Game Row

Example of a game row (deck and player IDs are hashed):

```python
game_data_example = {
    "created_at": "2025-11-03 02:00:29",
    
    "deck1_id_hash": "8ce52e72ce8e23e9ba40e65b21cb74232ad01e5f683dab81552751cf61bf1c87",
    "deck1_json": {
        "turns": 5,
        "gameId": 1457651,
        "result": 0,
        "winner": 2,
        "gameName": "3046621",
        "yourTime": "550",
        "character": [
            {"cardId": "cindra_dracai_of_retribution", "cardName": "Cindra, Dracai of Retribution", "numCopies": 1},
            ...
        ],
        "cardResults": [
            {"cardId": "ancestral_empowerment_red", "played": 0, "hits": 0},
            ...
        ],
        "turnResults": {
            "0": {"cardsUsed": 0, "damageDealt": 0, "damageTaken": 4},
            ...
        },
        "playerHero": "cindra_dracai_of_retribution",
        "opposingHero": "oscilio_constella_intelligence",
        "totalDamageDealt": 36,
        ...
    },
    
    "deck2_id_hash": "f2a895bd5cebeaa146ae1ed87f2e29f3b40cc433e616715eb5954ceac1004c1f",
    "deck2_json": {
        "turns": 5,
        "gameId": 1457651,
        "result": 1,
        "winner": 2,
        "gameName": "3046621",
        "yourTime": "610",
        "character": [
            {"cardId": "oscilio_constella_intelligence", "cardName": "Oscilio, Constella Intelligence", "numCopies": 1},
            ...
        ],
        "cardResults": [
            {"cardId": "blast_to_oblivion_red", "played": 0, "hits": 0},
            ...
        ],
        "turnResults": {
            "0": {"cardsUsed": 2, "damageDealt": 4, "damageTaken": 0},
            ...
        },
        "playerHero": "oscilio_constella_intelligence",
        "opposingHero": "cindra_dracai_of_retribution",
        "totalDamageDealt": 40,
        ...
    },
    
    "format": 0,
    "game_id": 1457651,
    "player1_name": "f3c0a079f77d425787e0b4d875858c22fe855326f94010026cd13f043b38cad9",
    "player2_name": "5bc1c30eaab47dc8c6cf5878a98f79279850f34a2bc0d7de30613777675967f6"
}
```

## ⚙️ Configuration

### Setting Your API Key

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   FUNCTION_API_KEY=your_actual_api_key_here
   ```

### Date Format
Always use `YYYY-MM-DD` format:
- ✅ `"2025-06-15"`
- ❌ `"1/15/2025"` or `"15-01-2025"`

**Important:** The database contains data from **June 2025** onwards. Use dates from June 2025 or later.

## 🆘 Troubleshooting

### "FUNCTION_API_KEY not found"
- Make sure you created a `.env` file
- Check that your API key is correct
- Make sure there are no extra spaces in your `.env` file

### "API Error: 401" 
- Your API key is wrong or expired
- Contact the maintainer for a new key

### "No data found"
- **Make sure your dates are from June 2025 or later** (data is available from June 2025 onwards)
- Try a different date range
- Check that the format code is correct
- Make sure there were games played on those dates

### "Download failed"
- Check your internet connection
- The download URL might have expired (try again)

## 📋 Requirements

- Python 3.7 or higher
- Internet connection
- Valid API key

## 🤝 Getting Help

1. Check the examples in the `examples/` folder
2. Look at the error messages - they usually tell you what's wrong
3. Contact the repository maintainer for API key issues

## 📄 License

This project is for educational and research purposes. Please respect data usage terms and privacy considerations.
This API is in no way affiliated with Legend Story Studios.  
Legend Story Studios®, Flesh and Blood™, and set names are trademarks of Legend Story Studios.  
Flesh and Blood characters, cards, logos, and art are property of Legend Story Studios.

---

**Ready to download data?** Start with `examples/download_csv_single_day.py`! 🎉
