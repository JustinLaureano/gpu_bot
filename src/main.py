from dotenv import load_dotenv
from functions import check_status, is_valid_check_time, send_email_notification
import logging
import os
import sys
import time

# Allows use of environment variables
load_dotenv()

# Basic logging config
logging.basicConfig(
    filename='./logs/_status.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

def gpu_bot():
    """
        Will request the gpu page source and determine
        if the gpu is currently for sale or in stock.
        Will only check during known times that new
        cards come into stock.
    """

    while True:
        # Make sure the time of day and week make sense to check
        if not is_valid_check_time():
            time.sleep(60 * 10) # ten minutes before checking again
            continue

        try:
            # Get the in stock status of the gpu
            status = check_status()
        except Exception as ex:
            # Log and quit if error occurs
            logging.error(ex)
            sys.exit(ex)

        # Log the status that was returned
        logging.info(status)

        # Check to see if its our lucky day
        if status == 'IN_STOCK' or status == 'ADD_TO_CART':
            # We need to send a notification now
            res = send_email_notification()

            # Log the email response, good or bad
            logging.info(res.message) if res.status == 1 else logging.error(res.message)

            if res.status < 1:
                # Handle email failure
                sys.exit(res.message)

        # Sleep between each check
        time.sleep(int(os.getenv('CHECK_STATUS_INTERVAL')))

# Start bot
gpu_bot()
