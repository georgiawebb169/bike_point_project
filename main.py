"""
Main orchestration script for the TfL BikePoint EL (Extract & Load) pipeline.
Fetches live Santander Cycles docking station data from the TfL API, saves it 
locally as a timestamped JSON file, and uploads it to an AWS S3 bucket.
"""

from datetime import datetime #allows me to access the datetime class in the datetime module 
import os #allows me to access the classes in the os module
from dotenv import load_dotenv #allows me to access the load_dotenv class from the dotenv 

# Import custom helper functions from our local 'modules' folder
from modules.extract_function import extract_to_json
from modules.loading_function import load_to_s3
from modules.logging_function import setup_logger

# ---------------------------------------------------------------------------
# 1. SETUP & LOGGING
# ---------------------------------------------------------------------------
# Capture the exact run time to use as a unique filename for both logs and data
#create 2 variables; timestamp and log_dir
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs'

# Start the logger first so all subsequent steps (and any errors) are recorded
# Call your custom setup logger function which takes timestamp and log_dirs parameters
logger = setup_logger(timestamp, log_dir)
logger.info('Logger initialised') #write logger initialised to my .log file inside the logs/ folder. 

# ---------------------------------------------------------------------------
# 2. EXTRACT (API -> Local JSON)
# ---------------------------------------------------------------------------
url = 'https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'

# Call the TfL API and save the response as 'data/<timestamp>.json'.
# If TfL's server throws a 5xx error, wait 10 seconds and retry up to 3 times.
# Call my custom function that takes these 5 parameters. 
extract_to_json(
    url,
    data_dir,
    timestamp,
    max_retry=3,
    delay=10
)

# ---------------------------------------------------------------------------
# 3. LOAD (Local JSON -> AWS S3)
# ---------------------------------------------------------------------------
# Load secrets from a local '.env' file if running on your own machine.
# (When running on GitHub Actions, these variables are injected automatically.)
load_dotenv()

# Pull AWS credentials and target bucket name from environment variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Upload everything in 'data/' to S3, then delete the local JSON files on success
load_to_s3(
    AWS_ACCESS_KEY,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
    data_dir
)
