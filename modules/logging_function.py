import logging 
import os

logger = logging.getLogger(__name__)

def setup_logger(timestamp:str, log_dir:str):
    """
    This initializes the logger for everything 

    Args:
        timestamp (str): for the filename of the logs.
        log_dir (str) where the logs shouldd be stored
    """
    os.makedirs(log_dir,exist_ok=True)
    log_filename=f'{log_dir}/{timestamp}.log'

    logging.basicConfig(
            filename=log_filename,
            format = '%(asctime)s - %(name)s - %(levelname)s %(message)s',
            level=logging.INFO
    )

    return logging.getLogger()