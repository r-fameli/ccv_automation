""" Google Sheets Task

Used to handle all interactions with Google Sheets
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def add_user_to_google_sheets( username: str, sheets_string: str) -> None:
    """ Reminds the user to add the individual to the Google Sheets
    
    Args:
        username (str): the username of the user to add to the sheet
        sheet_string(str): the string to be inserted into Google Sheets
    Returns:
        None
    """
    # TODO Check that user has not already been added to Google Sheets
    # Copy last line in application to bottom sheet and split text to columns
    # Check for PI email in pi_lookup sheet
    input("Add user " + username + " to the Google Sheet (remember to check for PI in pi_lookup). Press enter once completed")