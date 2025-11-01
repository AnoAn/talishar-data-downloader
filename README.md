# FaB Insights Talishar Data Downloader

A **community-supported** Python tool to download public Flesh and Blood game data from [Talishar](https://talishar.net).

> **No data is sold.** This project runs on **voluntary cost-sharing** via [Metafy](https://metafy.gg/@fabinsights) — to cover the server costs (Azure for the API + Hetzner for hosting the database).  
> Every supporter keeps the data flowing for the entire FaB community.

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

### 3. Choose Your Format and Dates
Open `examples/simple_download.py` and modify these lines:
```python
START_DATE = "2025-01-01"  # Your start date
END_DATE = "2025-01-03"    # Your end date  
FORMAT_CODE = "0"          # Game format (see table below)
```

### 4. Download Data
```bash
# Run the simple example
python examples/simple_download.py
```

That's it! Your data will be saved in the `data/` folder.


## 📁 What's Included

```
fab-talishar-data-download/
├── examples/
│   ├── simple_download.py      # 👈 Start here! Easy to copy and modify
├── src/
│   └── talishar_downloader/    # The main code (you don't need to touch this)
├── data/                       # Your downloaded files go here
├── .env.example               # Template for your API key
├── requirements.txt           # Python dependencies
└── README.md                 # This file
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
| "-1" | Clash |

## 📝 How to Use

### Option 1: Copy the Simple Script

1. Open `examples/simple_download.py`
2. Change these lines to what you want:
   ```python
   START_DATE = "2025-01-01"  # Your start date
   END_DATE = "2025-01-03"    # Your end date  
   FORMAT_CODE = "0"          # Format code (see table above)
   ```
   _Note:_ max 3 days per call.

3. Run: `python examples/simple_download.py`

### Option 2: Use the Code in Your Own Script

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
    start_date="2025-01-01",
    end_date="2025-01-03", 
    format_code="0",  # Classic Constructed
    output_dir="my_data"
)

if success:
    print("Download complete!")
```

### Option 3: Direct API Calls

If you want to call the API directly without using the Python library:

#### cURL Examples

**Download Classic Constructed data for a date range:**
```bash
# Step 1: Get download URL
curl -X GET "https://fab-insights.azurewebsites.net/api/get_results_blob?format=0&start_date=2025-01-01&end_date=2025-01-03" \
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


#### Python requests Example

```python
import requests

# Your API key
api_key = "YOUR_API_KEY"

# Step 1: Get download URL
response = requests.get(
    "https://fab-insights.azurewebsites.net/api/get_results_blob",
    params={
        "format": "0",  # Classic Constructed
        "start_date": "2025-01-01",
        "end_date": "2025-01-03"
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
- ✅ `"2025-01-15"`
- ❌ `"1/15/2025"` or `"15-01-2025"`

## 🆘 Troubleshooting

### "FUNCTION_API_KEY not found"
- Make sure you created a `.env` file
- Check that your API key is correct
- Make sure there are no extra spaces in your `.env` file

### "API Error: 401" 
- Your API key is wrong or expired
- Contact the maintainer for a new key

### "No data found"
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

**Ready to download data?** Start with `examples/simple_download.py`! 🎉
