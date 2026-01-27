import logging
import os
from datetime import datetime
from pathlib import Path
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file_name=os.path.join(LOG_DIR,f"log_{datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(
    filename=log_file_name,
    level=logging.INFO,
    format='[%(asctime)s]: %(levelname)s: %(message)s',
    filemode='a'
)
def get_logger(name: str) -> logging.Logger:
    """Function to get a logger instance.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    return logger
    
