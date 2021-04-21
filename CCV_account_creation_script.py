
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
#driver = webDriver.Firefox

your_username = ""
your_email = "riki_fameli@brown.edu"
brown_password = ""
listserv_password = ""

class YourInfo:
    def __init__(self, username, email, brown_password, listserv_password):
        self.username = username
        self.email = email
        self.brown_password = brown_password
        self.listserv_password = listserv_password

    def update_listserv_password(self, new_listserv_password):
        self.listserv_password = new_listserv_password

    def update_brown_password(self, new_brown_password):
        self.brown_password = new_brown_password

class UserInfo:
    def __init__(self, username, email):
        self.username = username
        self.email = email


def main():
    # your_username = "rfameli1"
    # your_email = "riki_fameli@brown.edu"
    # brown_password = ""
    # listserv_password = ""
    brown_password = getpass.getpass(prompt="Your Brown password: ")
    listserv_password = getpass.getpass(prompt="Your listserv password: ")

    your_info = YourInfo("rfameli1", "riki_fameli@brown.edu", brown_password, listserv_password)

    #user_id = input("User id")
    user_email = input("User email: ")

    add_user_to_grouper(your_info, user_email)
    add_user_to_listserv(your_info, user_email)
    # add_user_to_listserv(your_email, listserv_password, user_email)

    # email = input("Your email: ")
    # brown_password = getpass.getpass(prompt="Your Brown password (will not be stored): ")
    


    # NOTIFY USER
    # driver.get("https://groups.brown.edu/grouper/browseStemsAll.do")
    # driver.find_element_by_xpath("//*[@id=\"Content\"]/div[2]/div[2]/div[2]/ul/li[3]/a/span").click()
    # driver.find_element_by_xpath("")
    # driver.get("https://groups.brown.edu/grouper/populateGroupSummary.do?groupId=a815bed6b1ae442d9d4df08c4f3d61ff")
    # driver.get("https://groups.brown.edu/grouper/populateFindNewMembers.do?extension=ALL&displayNameDb=BROWN%3ASERVICES%3AHPC%3AALL&displayName=BROWN%3ASERVICES%3AHPC%3AALL&typeOfGroupDb=group&groupId=a815bed6b1ae442d9d4df08c4f3d61ff&description=&stemId=7d3f0eb75c2c4e1f9f95a9e5128f1d2b&subjectType=group&uuid=a815bed6b1ae442d9d4df08c4f3d61ff&subjectId=a815bed6b1ae442d9d4df08c4f3d61ff&modifierUuid=912ee0429eac4947894109787475a30a&displayExtensionDb=ALL&nameDb=BROWN%3ASERVICES%3AHPC%3AALL&parentStemName=BROWN%3ASERVICES%3AHPC&id=a815bed6b1ae442d9d4df08c4f3d61ff&group=Group%5Bname%3DBROWN%3ASERVICES%3AHPC%3AALL%2Cuuid%3Da815bed6b1ae442d9d4df08c4f3d61ff%5D&creatorUuid=7c3179121b454e9b8efea1865b1732cf&alternateName=&contextId=0b4d123a937a444baf22a65fd63f4c1b&parentUuid=7d3f0eb75c2c4e1f9f95a9e5128f1d2b&displayExtension=ALL&groupName=ALL&name=BROWN%3ASERVICES%3AHPC%3AALL&extensionDb=ALL&isGroup=true&alternateNameDb=&descriptionDb=&desc=ALL")


def add_user_to_grouper(your_info, search_term):
    driver.get("https://groups.brown.edu")

    automatic_login = confirm_action("Would you like to be logged in automatically? (y/n)")

    # Log into Grouper
    while "Grouper, the Internet2 groups" not in driver.title:
        # Attempt to log in automatically
        if automatic_login:
            WebDriverWait(driver, 30).until(EC.title_contains("Brown University"))
            driver.find_element_by_xpath("//input[@value='Brown Account Login']").click()
            username_box = driver.find_element_by_id("username")
            password_box = driver.find_element_by_id("password")
            username_box.clear()
            username_box.send_keys(your_info.username)
            password_box.clear()
            password_box.send_keys(your_info.brown_password)
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


def add_user_to_listserv(your_info, user_email):
    print("add user to listserv")

    automatic_login = True #confirm_automatic_login

    driver.get("https://listserv.brown.edu/")
    login_cell = driver.find_element_by_id("login.cell")
    
    while "Logged in as:" not in driver.page_source:
        if automatic_login:
            # https://listserv.brown.edu/cgi-bin/wa?LOGON
            login_cell = driver.find_element_by_id("login.cell")
            login_cell.click()
            email_input_box = driver.find_element_by_id("Email Address")
            email_input_box.clear()
            email_input_box.send_keys(your_info.email)
            password_input_box = driver.find_element_by_id("Password")
            # password_input_box = driver.find_element_by_css_selector("input[@type=password]")
            password_input_box.clear()
            password_input_box.send_keys(your_info.listserv_password)
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
            print("Waiting for listserv login")
            # continually check for logout.cell/login.cell
            # TODO

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
            print("Failed to add user to list")
    #logged_in_listserv = driver.find_elements_by_xpath("//*[contains(text(),'Logged in as: ')]").length() != 0
    # time.sleep(3)
    # while True:
    #     logged_in_listserv = "Logged in as:" in driver.page_source
    #     if not logged_in_listserv:
    #         input("Log into listserv, and then press a key")
    #     else:
    #         break

    # listserv_login = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table[1]/tbody/tr/td[1]/table/tbody/tr/td")




def confirm_action(message):
    """ Presents a simple confirmation message and returns True if the input is 'y' or 'yes', returns False otherwise"""
    automatic_login_response = input(message).casefold()
    return (automatic_login_response == "y" or automatic_login_response == "yes")



main()


#time.sleep(50)
#driver.quit()

# listserv_search = driver.find_element_by_id("Access Unlisted Lists")
# listserv_search.clear()
# listserv_search.send_keys("CCV")
# listserv_search.send_keys(Keys.RETURN)



