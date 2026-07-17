from pathlib import Path

ACCOUNTS = [
    # "creators.almanac",
    # "forever.a.teenager",
    "forever.animated",
    # "the.cinema.kingdom"
]

HEADLESS = False
ACTION_DELAY = 2
MAX_SCROLLS = 50
DAYS_TO_FETCH = 7

BASE_DIR = Path(__file__).resolve().parent

SESSION_FILE = BASE_DIR / "sessions" / "instagram.json"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)