import os

# Load environment variables
TAG_PAIRS = os.getenv("TAG_PAIRS", "1473_04_AS01_VS01_GT101_CSP,").split(",")

BASE_URL = os.getenv("BASE_URL", "https://webport.it.pitea.se/api")
API_KEY = os.getenv("API_KEY", "")
FIXED_OFFSET = os.getenv("FIXED_OFFSET", "+02:00")

BUFFER_SIZE = int(os.getenv("BUFFER_SIZE", 12))
ANOMALY_STD_MULTIPLIER = float(os.getenv("ANOMALY_STD_MULTIPLIER", 3))
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 300))  # in seconds
