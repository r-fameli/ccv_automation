import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def confirm_action(message: str) -> bool:
    """ Presents a simple confirmation message and returns True if the input is 'y' or 'yes', returns False otherwise
    
    Args:
        message (str): the message to be presented to the user
    Returns:
        bool: True if the user inputs 'y' or 'yes'. Otherwise false
    """
    automatic_login_response = input(message).casefold()
    return (automatic_login_response == "y" or automatic_login_response == "yes")

def timeout_action(driver_in_use: webdriver) -> None:
    """ Prints a timeout statement to the user and closes the driver and program 
    
    Args:
        driver_in_use (WebDriver): the driver that is currently being used
    Returns:
        None
    """
    print("Action failed to complete in time, closing driver")
    driver_in_use.close()
    sys.exit(1)
