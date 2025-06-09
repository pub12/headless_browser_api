"""
Application settings and configuration
"""
import os
import configparser
from pathlib import Path
from dotenv import load_dotenv
from app.core.logger import setup_logger

# Configure logger
logger = setup_logger()

# Load environment variables
load_dotenv()

# Load settings from INI file
config = configparser.ConfigParser()
config_path = Path(__file__).parent / "settings.ini"
if config_path.exists():
    config.read(config_path)
    logger.info(f"Loaded configuration from {config_path}")
else:
    logger.warning(f"Configuration file {config_path} not found. Using defaults.")
    # Set default values
    config["browser"] = {
        "ignore_https_errors": "True",
        "preserve_img_tags": "True"
    }
    config["api"] = {
        "title": "Hello World API",
        "port": "4113",
        "host": "0.0.0.0"
    }

# Browser settings
IGNORE_HTTPS_ERRORS = config.getboolean("browser", "ignore_https_errors", fallback=True)
PRESERVE_IMG_TAGS = config.getboolean("browser", "preserve_img_tags", fallback=True)
logger.info(f"Ignore HTTPS errors: {IGNORE_HTTPS_ERRORS}")
logger.info(f"Preserve img tags: {PRESERVE_IMG_TAGS}")

# API settings
API_TITLE = config.get("api", "title", fallback="Hello World API")
API_PORT = config.getint("api", "port", fallback=4113)
API_HOST = config.get("api", "host", fallback="0.0.0.0")

# Get approved IPs from environment variable
APPROVED_IPS = os.getenv("APPROVED_IPS", "").split(",")
logger.info(f"Approved IPs: {APPROVED_IPS}") 