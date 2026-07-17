# Instagram Reels Analytics

A Python + Playwright automation tool that scrapes Instagram Reels analytics from public creator accounts.

The script collects reels posted within the last **N days** (configurable), extracts analytics, and exports everything into a neatly formatted Excel report.

---

# Features

- Scrapes multiple Instagram accounts
- Collects only Reels (not posts)
- Filters reels from the last X days
- Extracts:
  - Posted Date
  - Views
  - Likes
  - Reel URL
- Exports data to Excel
- Separate worksheet for each account
- Automatically sorts reels by Views
- Reusable Instagram login session (no login every run)

---

# Folder Structure

```
instagram-analytics/
│
├── config.py
├── main.py
├── scraper.py
├── excel.py
├── models.py
├── utils.py
│
├── sessions/
│   └── instagram.json
│
├── reports/
├── screenshots/
├── logs/
├── data/
│
├── requirements.txt
└── README.md
```

---

# Requirements

- Python 3.11+
- Google Chrome
- Git

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/LikhithKumar105/instagram_scraping_profiles.git

cd instagram_scraping_profiles
```

---

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv venv
```

### Windows

```bash
python -m venv venv
```

---

## 3. Activate the virtual environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```cmd
venv\Scripts\activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Install Playwright browser

```bash
playwright install chromium
```

---

# First Time Login

Instagram blocks anonymous scraping.

The first time you run the project you need to create a logged-in session.

If a helper script such as `login.py` is included in the repository:

```bash
python login.py
```

A browser opens.

1. Log into Instagram.
2. Complete 2FA if required.
3. Wait until login finishes.
4. Close the browser.

A session file will be saved:

```
sessions/
    instagram.json
```

Every future run uses this session automatically.

---

# Configure Accounts

Open:

```
config.py
```

Edit:

```python
ACCOUNTS = [
    "creators.almanac",
    "forever.a.teenager",
    "forever.animated",
]
```

Add or remove usernames as needed.

---

# Configure Number of Days

In `config.py`

```python
DAYS_TO_FETCH = 7
```

Examples:

```
7
```

Last 7 days

```
30
```

Last 30 days

```
1
```

Only today's reels

---

# Run

```bash
python main.py
```

The scraper will:

- Open Account #1
- Collect reels
- Open every reel
- Extract analytics
- Stop when it reaches older reels
- Move to next account
- Export Excel

---

# Output

Reports are saved automatically inside

```
reports/
```

Example

```
Instagram_Analytics_20260717_193422.xlsx
```

Each account gets its own worksheet.

Columns include:

| Posted Date | Views | Likes | Views (Text) | Likes (Text) | Reel URL |
|-------------|-------|-------|--------------|--------------|----------|

---

# Configuration

Inside `config.py`

```python
HEADLESS = False
```

Set to

```python
HEADLESS = True
```

to run without opening the browser.

---

```python
ACTION_DELAY = 2
```

Increase this if Instagram loads slowly.

---

```python
MAX_SCROLLS = 50
```

Maximum number of scrolls before stopping.

---

# How It Works

For every account:

1. Opens the Reels tab.
2. Reads visible reels.
3. Opens each reel in a separate tab.
4. Extracts:
   - Posting date
   - Views
   - Likes
5. Checks whether the reel was posted within `DAYS_TO_FETCH`.
6. Stops when it encounters older reels.
7. Saves all recent reels to Excel.

---

# Notes

- Only public Instagram accounts are supported.
- An Instagram login session is required.
- Excessive scraping may trigger Instagram rate limits.
- If Instagram changes its HTML structure, selectors may need to be updated.

---

# Troubleshooting

### Session expired

Delete:

```
sessions/instagram.json
```

Run the login script again.

---

### Playwright browser missing

```bash
playwright install chromium
```

---

### Module not found

Activate the virtual environment first.

```bash
source venv/bin/activate
```

Then install requirements.

```bash
pip install -r requirements.txt
```

---

### Instagram blocks requests

Wait a few minutes before running again.

Reduce scraping speed by increasing:

```python
ACTION_DELAY
```

---

# Tech Stack

- Python
- Playwright
- OpenPyXL
- Dataclasses

---

# Future Improvements

- Comments extraction
- Shares extraction
- Caption extraction
- Thumbnail download
- Video duration
- CSV export
- Database support
- Automatic scheduling
- Email reports

---

# Disclaimer

This project is intended for educational and research purposes only.

Please ensure your usage complies with Instagram's Terms of Service.