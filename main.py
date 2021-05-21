""" CCV Ticket Creation Script

This script will automate many of the browser-based processes for creating new users for 
CCV's Oscar service.
"""
# python imports
import sys
import time
import getpass
import re

# local file imports
from utils import confirm_action, timeout_action, prompt_to_choose_option
from user_data import User, ProgramSettings

from grouper import add_user_to_grouper
from listserv import add_user_to_listserv
from webmin import add_user_in_webmin
from sheets import add_user_to_google_sheets
from deskpro import  insert_into_deskpro, print_deskpro_notification_in_terminal

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager


def main():
    """ The main function of the program """    
    driver = choose_driver()
    # webmin_access = confirm_action("Would you like to automate Webmin tasks as well (Requires Oscar)? (y/n)")
    insert_into_deskpro = confirm_action("Would you like to have messages automatically inserted into Deskpro? (y/n)")
    webmin_access = False
    one_by_one = True
    # Start the loop
    if one_by_one:
        create_accounts_one_by_one(driver, webmin_access, insert_into_deskpro)

    # End the program by closing the driver
    driver.quit()


def create_accounts_one_by_one(driver: webdriver, webmin_access = False, deskpro_insertion = False):
    """ Creates user accounts one by one.

    Args:
        driver (webdriver): the browser driver to use
        webmin_access (bool): whether or not the user has access to webmin
        deskpro_insertion (bool): whether or not the user would like messages to be inserted automatically into Deskpro
    Returns:
        None
    """
    running = True
    while (running):
        print('''\n
        CREATING NEW USER ACCOUNT
        ==============================
        Paste the full string from Deskpro that holds the user's information (e.g. 4/20/2021 - 09:15,uname@brown.edu,Full Name,email@brown.edu,pi_email@brown.edu,123456789)pygame.examples.mask.main()
        (On Linux-based terminals, use Ctrl+Insert, Ctrl+Shift+V, or right click to paste)
        ''')
        # Example: 4/20/2021 - 09:15,rfameli1@brown.edu,Riki Fameli,riki_fameli@brown.edu,pi_email@brown.edu,620123553
        if deskpro_insertion:
            ticket_id = input("Insert ID of the ticket: ")
        next_user = receive_and_parse_account_str()
        add_user_to_google_sheets(next_user.username, "")
        if webmin_access:
            webmin_batch_string = input("Please enter the generated string for Webmin: ").strip()
        else:
            webmin_batch_string = ""
        add_user_in_webmin(driver, webmin_batch_string, next_user.username, webmin_access) # TODO add user in Webmin if possible, including priority groups if required
        add_user_to_grouper(driver, next_user.email)
        add_user_to_listserv(driver, next_user.email)
        if deskpro_insertion:
            insert_into_deskpro(driver, ticket_id, next_user)
        else:
            print_deskpro_notification_in_terminal(next_user)
        # generate_user_notification_html(next_user)
        # If more users need to be added, the loop will continue running
        running = confirm_action("Would you like to add another user? (y/n)")

def receive_and_parse_account_str() -> User:
    """ Asks the user for an account string, returning a User if it's valid and asking the user to re-input if it is not

    Returns:
        User: a User with the correct information
    """
    account_creation_strings = input("Account creation string: ").split(',')
    ask_for_reinput = lambda: input("Please input the corrected account string: ").split(',')
    while (True):
        if len(account_creation_strings) != 6:
            print("Account string must have 6 comma-separated fields")
            account_creation_strings = ask_for_reinput()
            continue
        user_id = account_creation_strings[1].split('@')[0]
        user_first_name = account_creation_strings[2].split(' ')[0]
        user_email = account_creation_strings[3]
        if user_id == "" or user_first_name == "" or user_email == "":
            print("One of the required fields is blank.")
            account_creation_strings = ask_for_reinput()
        else:
            return User(user_first_name, user_id, user_email)


def choose_driver():
    """ Asks the user for their browser preference and returns the corresponding browser driver if availablepygame.examples.mask.main()

    Returns:
        webdriver: either a ChromeDriver (Google Chrome) or a GeckoDriver (Firefox)
    """
    driver = None
    browser_preference = prompt_to_choose_option(
        "Which browser would you like to use? Type 'chrome' for Google Chrome or 'firefox' for Firefox (Firefox recommended): ",
        ["firefox", "chrome"]
    )
    if browser_preference == 'firefox':
        print("Initializing geckodriver for Firefox")
        driver = webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install())
    elif browser_preference == 'chrome':
        driver = webdriver.Chrome(ChromeDriverManager().install())
        print("Initializing ChromeDriver for Chrome...")
        print('''ChromeDriver may spam with unnecessary errors e.g. 'Failed to read descriptor from node connection'. 
        They can be ignored if the program is still running, but may obscure prompts''')

    return driver

main()


