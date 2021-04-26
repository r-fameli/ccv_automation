
import sys
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

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
    ''' The main function of the program '''
    print("Selenium will spam the terminal with unnecessary errors initially, so you may not see all the prompts")
    print("Please insert the following information as it is requested. Information will be stored only for use in the program.")

    automatic_login = confirm_action("Would you like to be logged in to services automatically (passwords will not be stored)? (y/n)")

    if (automatic_login):
        # Store the script user's info into a ScriptUserCredentials if they want to be logged in automatically
        your_email = input("Your email: ")
        your_username = input("Your username: ")
        brown_password = getpass.getpass(prompt="Your Brown password (will not show characters): ")
        listserv_password = getpass.getpass(prompt="Your listserv password (will not show characters): ")
        your_credentials = ScriptUserCredentials(your_username, your_email, brown_password, listserv_password)
    else:
        # if user does not want to be logged in automatically, set your_credentials to None
        your_credentials = None

    running = True
    while (running):
        print("Now input the requested information about the user whose account you are creating")
        user_id = input("User id: ")
        user_email = input("User email: ")
        user_first_name = input("User's first name: ")
        next_user = UserInfo(user_first_name, user_id, user_email)

        add_user_to_grouper(your_credentials, next_user.email)
        add_user_to_listserv(your_credentials, next_user.email)
        generate_user_notification(next_user)    
    
    # NOTIFY USER
    # driver.get("https://groups.brown.edu/grouper/browseStemsAll.do")
    # driver.get("https://groups.brown.edu/grouper/populateGroupSummary.do?groupId=a815bed6b1ae442d9d4df08c4f3d61ff")
    # driver.get("https://groups.brown.edu/grouper/populateFindNewMembers.do?extension=ALL&displayNameDb=BROWN%3ASERVICES%3AHPC%3AALL&displayName=BROWN%3ASERVICES%3AHPC%3AALL&typeOfGroupDb=group&groupId=a815bed6b1ae442d9d4df08c4f3d61ff&description=&stemId=7d3f0eb75c2c4e1f9f95a9e5128f1d2b&subjectType=group&uuid=a815bed6b1ae442d9d4df08c4f3d61ff&subjectId=a815bed6b1ae442d9d4df08c4f3d61ff&modifierUuid=912ee0429eac4947894109787475a30a&displayExtensionDb=ALL&nameDb=BROWN%3ASERVICES%3AHPC%3AALL&parentStemName=BROWN%3ASERVICES%3AHPC&id=a815bed6b1ae442d9d4df08c4f3d61ff&group=Group%5Bname%3DBROWN%3ASERVICES%3AHPC%3AALL%2Cuuid%3Da815bed6b1ae442d9d4df08c4f3d61ff%5D&creatorUuid=7c3179121b454e9b8efea1865b1732cf&alternateName=&contextId=0b4d123a937a444baf22a65fd63f4c1b&parentUuid=7d3f0eb75c2c4e1f9f95a9e5128f1d2b&displayExtension=ALL&groupName=ALL&name=BROWN%3ASERVICES%3AHPC%3AALL&extensionDb=ALL&isGroup=true&alternateNameDb=&descriptionDb=&desc=ALL")


def add_user_to_grouper(your_credentials, search_term):
    ''' Adds the user to the group Brown:Services:HPC using the provided search_term '''
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
            try: 
                driver.find_element_by_xpath("//button[@value='Login']").click()
                # Account for Duo login
                print("Waiting for secondary authentication (Will timeout after 20 seconds)")
                WebDriverWait(driver, 20).until(EC.title_contains("Grouper, the Internet2 groups"))
                print("Adding user to Grouper")
                break
            except:
                print("Automatic login failed, please login to Grouper manually")
                automatic_login = False
                continue
        else:
            # Log in to Grouper manually
            print("Waiting for Grouper login")
            WebDriverWait(driver, 60).until_not(EC.title_contains("Brown University"))
            WebDriverWait(driver, 30).until(EC.title_contains("Grouper, the Internet2 groups"))
            print("Logged in successfully")
            break
    
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


def add_user_to_listserv(your_credentials, user_email):
    ''' Adds the user to the CCV and CCV_ANNOUNCE listserv lists '''
    print("add user to listserv")

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
            # driver.find_element_by_xpath("//input[@type='submit' and value='Log In']").click()
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

    lists_to_add = ["CCV", "CCV_ANNOUNCE"]

    for list in lists_to_add:
        driver.get("https://listserv.brown.edu/cgi-bin/wa?ACTMGR1=" + list)
        driver.find_element_by_id("Do Not Notify the User").click()
        email_input_box = driver.find_element_by_id("Email Address and Name")
        email_input_box.clear()
        email_input_box.send_keys(user_email)
        email_input_box.send_keys(Keys.RETURN)

        if "already subscribed" in driver.page_source:
            print("User is already subscribed to list " + list)
        elif "has been added" in driver.page_source:
            print("User has been added to list " + list)
        else:
            print("Failed to add user to list" + list)

def generate_user_notification(user_info):
    """ Generates a message in HTML to send back to the user to notify them that their account has been created"""
    print(""" 
    <p></p><p><span></span></p><p></p><p></p><p></p><p>Hi {first_name},</p><p><br></p><p>Your Oscar account was created -
     you should be able to login with the same credentials as used for other Brown services. Let us know if you encounter any issues. 
     To access via terminal/command line: </p><p></p><pre class="dp-pre">ssh {username}@ssh.ccv.brown.edu
     </pre><p></p><p><span><span>
     Documentation for new users can be found at this link:&nbsp;</span><a href="https://docs.ccv.brown.edu/oscar/getting-started">
     <span>https://docs.ccv.brown.edu/oscar/getting-started</span></a><span>.</span></span></p><p><span><span>
     We offer workshops on using Oscar, upcoming sessions can be found at this link:&nbsp;</span><a href="https://events.brown.edu/ccv/view/all">
     <span>https://events.brown.edu/ccv/view/all</span></a></span></p><p><span><span><strong>Note: </strong>
     This account and all CCV systems fall under the Computing Policy for Brown University. You can review this policy at </span>
     <a href="https://it.brown.edu/computing-policies"><span>https://it.brown.edu/computing-policies</span></a></span></p><p><br></p>
     <p>Thank you,</p>
     <p><br></p>
     <p></p>
    """.format(first_name = user_info.first_name, username = user_info.username))

def confirm_action(message):
    """ Presents a simple confirmation message and returns True if the input is 'y' or 'yes', returns False otherwise """
    automatic_login_response = input(message).casefold()
    return (automatic_login_response == "y" or automatic_login_response == "yes")

def timeout_action(driver_in_use):
    """ Prints a timeout statement to the user and closes the driver and program """
    print("Action failed to complete in time, closing driver")
    driver_in_use.close()
    sys.exit(1)

main()


