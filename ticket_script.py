""" CCV Ticket Creation Script

This script will automate many of the browser-based processes for creating new users for 
CCV's Oscar service.
"""
import sys
import time
import getpass
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install())
driver = None #webdriver.Chrome(ChromeDriverManager().install())

class ScriptUserCredentials:
    """ Holds the information of the user using the script """
    def __init__(self, username, email, brown_password, listserv_password):
        """ Creates a new instance of ScriptUserInfo """
        self.username = username
        self.email = email
        self.brown_password = brown_password
        self.listserv_password = listserv_password

    def update_listserv_password(self, new_listserv_password):
        """ Updates the listserv password stored """
        self.listserv_password = new_listserv_password

    def update_brown_password(self, new_brown_password):
        """ Updates the Brown password stored """
        self.brown_password = new_brown_password

class UserInfo:
    """ Stores a user's information """
    def __init__(self, first_name, username, email):
        self.first_name = first_name
        self.username = username
        self.email = email


def main():
    """ The main function of the program """
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
            print("ChromeDriver may spam with unnecessary errors e.g. 'Failed to read descriptor from node connection'. They can be ignored if the program is still running, but may obscure prompts")
            driver = webdriver.Chrome(ChromeDriverManager().install())
            break
        else:
            browser_preference = input("Browser " + browser_preference + " is not an option. Options are chrome and firefox. Please type your choice: ")
    

    print("Please insert the following information as it is requested. Information will be stored only for use in the program.")

    automatic_login = confirm_action("Would you like to be logged in to services automatically (passwords will not be stored)? (y/n)")

    if (automatic_login):
        # Store the script user's info into a ScriptUserCredentials if they want to be logged in automatically
        print("BROWN LOGIN:")
        your_username = input("Your Brown username: ")
        brown_password = getpass.getpass(prompt="Your Brown password (will not show characters): ")
        print("LISTSERV LOGIN:")
        your_email = input("Your email: ")
        listserv_password = getpass.getpass(prompt="Your listserv password (will not show characters): ")
        your_credentials = ScriptUserCredentials(your_username, your_email, brown_password, listserv_password)
    else:
        # if user does not want to be logged in automatically, set your_credentials to None
        your_credentials = None

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

        next_user = UserInfo(user_first_name, user_id, user_email)

        add_user_to_google_sheets(next_user.username, "") # TODO
        add_user_in_webmin("", next_user.username) # TODO add user in Webmin if possible, including priority groups if required
        add_user_to_grouper(your_credentials, next_user.email)
        add_user_to_listserv(your_credentials, next_user.email)

        time.sleep(1)
        generate_user_notification_html(next_user)
        # If more users need to be added, the loop will continue running
        running = confirm_action("Would you like to add another user? (y/n)")
    
    # End the program by closing the driver
    driver.quit()


# def scrape_from_deskpro() -> list:
#     print("")
#     # TODO
#     # find last element where xpath is //div[@class='body-text-message unreset'] (ENSURE THAT ONLY ONE TAB IS OPEN IN DESKPRO)
#     # TO CLOSE ALL TABS:
#     # right click in //div[@class='deskproTabListInner ng-isolate-scope']
#     # click on //li[@ng-show='showCloseAll()']
#     # 


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

def add_user_in_webmin(batch_string_file: str, username: str) -> None:
    """ Adds the user in webmin using the batch job string 
    
    Args:
        batch_string_file (str): the string that will be used to create the user
        username(str): the user's AD username
    Returns:
        None
    """
    input("Add user " + username + " to Webmin. Press enter once completed")


def add_user_to_grouper(your_credentials: ScriptUserCredentials, search_term: str) -> None:
    """ Adds the user to the group Brown:Services:HPC using the provided search_term 
    
    Args:
        your_credentials (ScriptUserCredentials): the credentials of the person using the script (used for login)
        search_term (str): the string to search for in grouper (typically email or username)
    Returns:
        None
    """
    print("Adding user " + search_term + " to grouper")
    driver.get("https://groups.brown.edu")

    automatic_login = not (your_credentials == None)
    
    # Log into Grouper
    while "Grouper, the Internet2 groups" not in driver.title:
        # Attempt to log in automatically
        if automatic_login:
            WebDriverWait(driver, 30).until(EC.title_contains("Brown University"))
            driver.find_element_by_xpath("//input[@value='Brown Account Login']").click()
            username_box = driver.find_element_by_id("username")
            password_box = driver.find_element_by_id("password")
            username_box.clear()
            username_box.send_keys(your_credentials.username)
            password_box.clear()
            password_box.send_keys(your_credentials.brown_password)
            password_box.send_keys(Keys.RETURN)
            try: 
                # Account for Duo login
                print("Waiting for secondary authentication (Will timeout after 30 seconds)")
                WebDriverWait(driver, 30).until(EC.title_contains("Grouper, the Internet2 groups"))
                break
            except:
                print("Automatic login failed, please login to Grouper manually")
                automatic_login = False
                continue
        else:
            # Log in to Grouper manually
            print("Waiting for manual Grouper login")
            WebDriverWait(driver, 60).until_not(EC.title_contains("Brown University"))
            WebDriverWait(driver, 30).until(EC.title_contains("Grouper, the Internet2 groups"))
            break

    print("Logged in successfully")
    
    # Search for the user in the Brown:Services:HPC group
    driver.get("https://groups.brown.edu/grouper/populateGroupSummary.do?groupId=a815bed6b1ae442d9d4df08c4f3d61ff")
    driver.find_element_by_xpath("//span[@class='grouperTooltip' and text()='Add members']").click()
    member_search = driver.find_element_by_id("searchTerm")
    member_search.clear()
    member_search.send_keys(search_term)
    member_search.send_keys(Keys.RETURN)

    # Check that there is only one user
    grouper_search_results = driver.find_elements_by_xpath("//fieldset/ul/li")
    if len(grouper_search_results) == 0:
        print(f"No users found with search term {0}".format(search_term))
        return False
    elif len(grouper_search_results) > 1:
        print(f"More than one user found with search term {0}".format(search_term))
        return False
    else:
        driver.find_element_by_xpath("//input[@class='blueButton' and @value='Assign privileges']").click()

    if "successfully assigned" in driver.page_source:
        print("Successfully added user in Grouper")
        return True


def add_user_to_listserv(your_credentials: ScriptUserCredentials, user_email: str) -> None:
    """ Adds the user to the CCV and CCV_ANNOUNCE listserv lists
    
    Args:
        your_credentials (ScriptUserCredentials): credentials of the script user for logging into listserv
        user_email (str): the email of the user
    Returns:
        None
    """
    print("Adding user email " + user_email + " to listserv")

    automatic_login = not (your_credentials == None)
    driver.get("https://listserv.brown.edu/")
    
    while "Logged in as:" not in driver.page_source:
        if automatic_login:
            driver.get("https://listserv.brown.edu/cgi-bin/wa?LOGON")
            email_input_box = driver.find_element_by_id("Email Address")
            email_input_box.clear()
            email_input_box.send_keys(your_credentials.email)
            password_input_box = driver.find_element_by_id("Password")
            password_input_box.clear()
            password_input_box.send_keys(your_credentials.listserv_password)
            password_input_box.send_keys(Keys.RETURN)
            try:
                WebDriverWait(driver, 10).until("Logged in as:" in driver.page_source)
                break
            except: 
                print("Automatic login failed, please login to listserv manually")
                automatic_login = False
                continue
        else:
            # Log in to Grouper manually
            try:
                print("Waiting for listserv login")
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "logout.cell")))
                break
            except:
                timeout_action(driver)

    print("Logged into listserv")
    lists_to_add = ["CCV", "CCV_ANNOUNCE"]

    for list in lists_to_add:
        driver.get("https://listserv.brown.edu/cgi-bin/wa?ACTMGR1=" + list)
        driver.find_element_by_id("Do Not Notify the User").click()
        email_input_box = driver.find_element_by_id("Email Address and Name")
        email_input_box.clear()
        email_input_box.send_keys(user_email)
        email_input_box.send_keys(Keys.RETURN)
        time.sleep(1)
        message = driver.find_element_by_xpath("//td[@class='message']")
        message_text = message.get_attribute('innerText')
        print(message_text)

        # if "already subscribed" in message_text:
        #     print("User is already subscribed to list " + list)
        # elif "has been added" in message_text:
        #     print("User has been added to list " + list)
        # else:
        #     print("Failed to add user to list " + list)

def generate_user_notification_html(user_info: UserInfo) -> None:
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

def confirm_action(message: str) -> bool:
    """ Presents a simple confirmation message and returns True if the input is 'y' or 'yes', returns False otherwise
    
    Args:
        message (str): the message to be presented to the user
    Returns:
        bool: True if the user inputs 'y' or 'yes'. Otherwise false
    """
    automatic_login_response = input(message).casefold()
    return (automatic_login_response == "y" or automatic_login_response == "yes")

def timeout_action(driver_in_use) -> None:
    """ Prints a timeout statement to the user and closes the driver and program 
    
    Args:
        driver_in_use (WebDriver): the driver that is currently being used
    Returns:
        None
    """
    print("Action failed to complete in time, closing driver")
    driver_in_use.close()
    sys.exit(1)

main()


