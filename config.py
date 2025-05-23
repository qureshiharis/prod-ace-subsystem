import os

# Load environment variables
TAG_PAIRS = os.getenv("TAG_PAIRS", "1473_04_AS01_VS01_GT101_CSP,").split(",")

BASE_URL = os.getenv("BASE_URL", "https://webport.it.pitea.se/api")
API_KEY = os.getenv("API_KEY", "")
FIXED_OFFSET = os.getenv("FIXED_OFFSET", "+02:00")

BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", 12))
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 300))  # in seconds

HISTORICAL_MODE = os.getenv("HISTORICAL_MODE", "false").lower() == "true"
HISTORICAL_DATA_DURATION_MINUTES = int(os.getenv("HISTORICAL_DATA_DURATION_MINUTES", 525600))  # in minutes
HISTORICAL_DATA_FETCH_FREQUENCY_DAYS = int(os.getenv("HISTORICAL_DATA_FETCH_FREQUENCY_DAYS", 7))  # in days; 