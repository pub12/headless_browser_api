"""
Logging configuration
"""
import logging

def setup_logger():
    """Configure and return a logger for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("api.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__) 