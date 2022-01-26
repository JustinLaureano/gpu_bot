from bs4 import BeautifulSoup
from datetime import datetime, time
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import smtplib

load_dotenv()

def is_valid_check_time():
    """
        Only want to check that the current date time
        is a weekday and during business hours (7am - 6pm)
    """
    now = datetime.now()

    return 0 <= now.weekday() <= 4 and time(7) <= now.time() <= time(18)


def check_status():
    """
        Check the gpu page to see if it is in stock or not
    """

    # Init web driver
    driver = webdriver.Remote("http://selenium-hub:4444/wd/hub", DesiredCapabilities.CHROME)

    # Fetch web page
    driver.get(os.getenv('BESTBUY_URL'))

    # Parse html
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close web driver
    driver.quit()

    # Get the status from the add to cart button and return it
    add_to_cart_btn = soup.find('button', class_='add-to-cart-button')

    # Handle any unexpected cases where the html is not as expected
    if add_to_cart_btn is None:
        return 'ADD_TO_CART_BUTTON_NOT_FOUND';

    # Get the in stock status
    # Hope it returns ADD_TO_CART or IN_STOCK
    status = add_to_cart_btn['data-button-state']

    return status


def send_email_notification():
    """
        Sends a notification that the gpu is in stock
    """

    # Structure email response
    message = (
        f"From: Justin <{os.getenv('GMAIL_ADDRESS')}>"
        f"To: Justin <{os.getenv('NOTIFICATION_ADDRESS')}>"
        f"Subject: GPU IN STOCK!"
        f"The Nvidia Geforce RTX 3080 10GB Founders Edition is now in stock at {os.getenv('BESTBUY_URL')}"
    )

    email_receivers = [os.getenv('NOTIFICATION_ADDRESS')]

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(os.getenv('GMAIL_ADDRESS'), os.getenv('GMAIL_PASSWORD'))
        server.sendmail(os.getenv('GMAIL_ADDRESS'), email_receivers, message)
        server.close()

        return {'status': 1, 'message': 'Successfully Sent Email'}
    except Exception as ex:
        return {'status': 0, 'message': ex}


def archive_log_file():
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")

    log_dir = '/usr/src/app/logs/'
    log_file_name = '_status.log'

    # copy the log file to a date prepended log file
    os.popen(f'cp {log_dir}{log_file_name} {log_dir}{date_time}{log_file_name}')

    # Truncate the log file
    with open(f'{log_dir}{log_file_name}', 'w'):
        pass
