import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    TEST_USERNAME = os.getenv("TEST_USERNAME", "")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", 30000))