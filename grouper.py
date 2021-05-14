""" Grouper Task

Used to handle all interactions with Grouper
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

from utils import timeout_action


def add_user_to_grouper(driver: webdriver, search_term: str) -> None:
    """ Adds the user to the group Brown:Services:HPC using the provided search_term 
    
    Args:
        your_credentials (ScriptUserCredentials): the credentials of the person using the script (used for login)
        search_term (str): the string to search for in grouper (typically email or username)
    Returns:
        None
    """
    print("Adding user " + search_term + " to grouper")
    driver.get("https://groups.brown.edu")

    
    # Log into Grouper
    while "Grouper, the Internet2 groups" not in driver.title:
        # Log in to Grouper manually
        print("Waiting for manual Grouper login (times out after 60 seconds)")
        try:

            WebDriverWait(driver, 60).until_not(EC.title_contains("Brown University"))
            WebDriverWait(driver, 30).until(EC.title_contains("Grouper, the Internet2 groups"))
            break
        except:
            timeout_action(driver)

    print("Logged in successfully")

    # Search for the user in the Brown:Services:HPC group
    driver.get("https://groups.brown.edu/grouper/populateGroupSummary.do?groupId=a815bed6b1ae442d9d4df08c4f3d61ff")
    driver.find_element_by_xpath("//span[@class='grouperTooltip' and text()='Add members']").click()
    member_search = driver.find_element_by_id("searchTerm")
    member_search.clear()
    member_search.send_keys(search_term)
    member_search.send_keys(Keys.RETURN)

    # Check that there is only one user
    # Lite UI: https://groups.brown.edu/grouper/grouperUi/appHtml/grouper.html?operation=Misc.index

    # Sleep momentarily so that everything can load
    time.sleep(2)
    grouper_search_results = driver.find_elements_by_xpath("//input[@name='members']")
    if len(grouper_search_results) == 0:
        input("No users found with search term " + search_term + ". Press enter to continue")
        return False
    if len(grouper_search_results) > 1:
        print("Multiple users found with search term" + search_term)
        input("Select the correct user and press enter")
        driver.find_element_by_xpath("//input[@class='blueButton' and @value='Assign privileges']").click()
    else:
        driver.find_element_by_xpath("//input[@class='blueButton' and @value='Assign privileges']").click()

    message = driver.find_element_by_xpath("//div[@class='Message']").get_attribute('innerText')
    print("GROUPER ==> " + message)
    input("Successfully added user " + search_term + " in Grouper. Press enter to continue")
    return True


# Uncomment and run this to test Grouper
# add_user_to_grouper(
#     webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install()),
#     "riki_fameli@brown.edu"
# )


# NEW UI
# https://groups.brown.edu/grouper/new
# Group management page:
# https://groups.brown.edu/grouper/grouperUi/app/UiV2Main.index?operation=UiV2Group.viewGroup&groupId=a815bed6b1ae442d9d4df08c4f3d61ff
# Add members page:
# https://groups.brown.edu/grouper/grouperUi/app/UiV2Main.index?operation=UiV2GroupImport.groupImport&groupId=a815bed6b1ae442d9d4df08c4f3d61ff&backTo=group

# OLD UI
# Group management page:
# https://groups.brown.edu/grouper/populateGroupSummary.do?groupId=a815bed6b1ae442d9d4df08c4f3d61ff
