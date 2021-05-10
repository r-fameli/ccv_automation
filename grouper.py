""" Grouper Task

Used to handle all interactions with Grouper
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from user_data import ScriptUserCredentials


def add_user_to_grouper(driver: webdriver, your_credentials: ScriptUserCredentials, search_term: str) -> None:
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
