""" CCV Ticket Creation Script

This script will automate many of the browser-based processes for creating new users for 
CCV's Oscar service.
"""
import sys
import time
import getpass
import re

# local file imports
from utils import confirm_action, timeout_action
from user_data import User

from grouper import add_user_to_grouper
from listserv import add_user_to_listserv
from webmin import add_user_in_webmin
from sheets import add_user_to_google_sheets

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
    # print("Please insert the following information as it is requested. Information will be stored only for use in the program.")

    # Start the loop
    running = True
    while (running):
        print('''\n
        CREATING NEW USER ACCOUNT
        ==============================
        Copy the full string from Deskpro that holds the user's information (e.g. 4/20/2021 - 09:15,uname@brown.edu,Full Name,email@brown.edu,pi_email@brown.edu,123456789)
        ''')
        # Example: 4/20/2021 - 09:15,rfameli1@brown.edu,Riki Fameli,riki_fameli@brown.edu,pi_email@brown.edu,620123553
        account_creation_strings = input("Account creation string: ").split(',')
        user_id = account_creation_strings[1].split('@')[0]
        user_first_name = account_creation_strings[2].split(' ')[0]
        user_email = account_creation_strings[3]


        next_user = User(user_first_name, user_id, user_email)

        add_user_to_google_sheets(next_user.username, "") # TODO
        add_user_in_webmin("", next_user.username) # TODO add user in Webmin if possible, including priority groups if required
        add_user_to_grouper(driver, next_user.email)
        add_user_to_listserv(driver, next_user.email)

        time.sleep(1)
        generate_user_notification_html(next_user)
        # If more users need to be added, the loop will continue running
        running = confirm_action("Would you like to add another user? (y/n)")
    
    # End the program by closing the driver
    driver.quit()


def choose_driver():
    """ Asks the user for their browser preference and returns the corresponding browser driver if availablepygame.examples.mask.main()

    Returns:
        webdriver: either a ChromeDriver (Google Chrome) or a GeckoDriver (Firefox)
    """
    driver = None
    browser_preference = input(
            "Which browser would you like to use? Type 'chrome' for Google Chrome or 'firefox' for Firefox (Firefox recommended): "
            ).strip().casefold()
    while True:
        if browser_preference == 'firefox':
            print("Initializing geckodriver for Firefox")
            driver = webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install())
            break
        elif browser_preference == 'chrome':
            print("Initializing ChromeDriver for Chrome...")
            print('''ChromeDriver may spam with unnecessary errors e.g. 'Failed to read descriptor from node connection'. 
            They can be ignored if the program is still running, but may obscure prompts''')
            driver = webdriver.Chrome(ChromeDriverManager().install())
            break
        else:
            browser_preference = input("Browser " + browser_preference + " is not an option. Options are chrome and firefox. Please type your choice: ")
    return driver

def generate_user_notification_html(user_info: User) -> None:
    """ Generates a message in HTML to send back to the user in Deskpro to notify them that their account has been created

    Args:
        user_info (UserInfo): the information of the user that stores their name and username
    Returns:
        None: prints an HTML string that can be input using Deskpro's html feature
    """
    print(""" 

    NOTIFY USER
    ==============================

    <p></p><p><span></span></p><p></p><p></p><p></p><p>Hi {first_name},</p><p><br></p><p>Your Oscar account was created -
     you should be able to login with the same credentials as used for other Brown services. Let us know if you encounter any issues. 
     To access via terminal/command line: </p><p></p><pre class="dp-pre">ssh {username}@ssh.ccv.brown.edu</pre><p>
     Documentation for new users can be found at this link:&nbsp;</span><a href="https://docs.ccv.brown.edu/oscar/getting-started">
     <span>https://docs.ccv.brown.edu/oscar/getting-started</span></a><span>.</span></span></p><p><span><span>
     We offer workshops on using Oscar, upcoming sessions can be found at this link:&nbsp;</span><a href="https://events.brown.edu/ccv/view/all">
     <span>https://events.brown.edu/ccv/view/all</span></a></span></p><p><span><span><strong>Note: </strong>
     This account and all CCV systems fall under the Computing Policy for Brown University. You can review this policy at </span>
     <a href="https://it.brown.edu/computing-policies"><span>https://it.brown.edu/computing-policies</span></a></span></p><p><br></p>
     <p>Thank you,</p>
     <p><br></p>
     <p></p>

     ==============================
    """.format(first_name = user_info.first_name, username = user_info.username))
    input('''In Deskpro, select the option to insert using HTML and paste the above message in. Then turn off the HTML setting.
     Press enter once you have added your name and sent the message.''')

main()


