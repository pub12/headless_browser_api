"""
Application settings and configuration
"""
import os
from dotenv import load_dotenv
from app.core.logger import setup_logger

# Configure logger
logger = setup_logger()

# Load environment variables
load_dotenv()

# API settings
API_TITLE = "Hello World API"
API_PORT = 4113
API_HOST = "0.0.0.0"

# Get approved IPs from environment variable
APPROVED_IPS = os.getenv("APPROVED_IPS", "").split(",")
logger.info(f"Approved IPs: {APPROVED_IPS}") 