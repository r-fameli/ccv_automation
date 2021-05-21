""" Grouper Task

Used to handle all interactions with Grouper
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException

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
        except TimeoutException as ex:
            timeout_action(driver)

    print("Logged in successfully")

    try:
        # Search for the user in the Brown:Services:HPC group
        driver.get("https://groups.brown.edu/grouper/grouperUi/appHtml/grouper.html?operation=SimpleMembershipUpdate.init&groupId=a815bed6b1ae442d9d4df08c4f3d61ff")
        search_bar_xpath = "//input[@class='dhx_combo_input']"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_bar_xpath)))
        search_bar = driver.find_element_by_xpath(search_bar_xpath)
        search_bar.clear()
        search_bar.send_keys(search_term)

        dropdown_option_xpath = "//div[@class='dhx_combo_list ']/div"
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, dropdown_option_xpath)))
        grouper_search_results = driver.find_elements_by_xpath(dropdown_option_xpath)
        if len(grouper_search_results) == 0:
            input("No users found with search term " + search_term + ". Press enter to continue")
            return False
        elif len(grouper_search_results) > 1:
            print("Multiple users found with search term" + search_term)
            print("Please click the correct user from the dropdown (will timeout after 60 seconds)")
            # Wait until the dropdown menu is hidden
            WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='dhx_combo_list '][2]")))
        else:
            user_option = driver.find_element_by_xpath(dropdown_option_xpath + "/div")
            user_info = user_option.get_attribute('innerText')
            print("Found user " + user_info)
            user_option.click()

        driver.find_element_by_xpath("//input[@name='addMemberButton']").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "simplemodal-data")))
        message = driver.find_element_by_id("simplemodal-data").get_attribute('innerText')
        if message.endswith('OK'):
            message = message[:-2]
        print("GROUPER ==> " + message)
        input("Press enter to continue.")

        # Close the popup window
        # driver.find_element_by_xpath("//button[@class='simplemodal-close blueButton']").click()
    except TimeoutException as ex:
        print("ERROR: " + str(ex))
        print("Closing browser.")
        timeout_action(driver)

# TESTS
# Uncomment these and run the file to test Grouper adding

# Single user
# add_user_to_grouper(
#     webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install()),
#     "riki_fameli@brown.edu"
# )

# Multiple users
# add_user_to_grouper(
#     webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install()),
#     "riki"
# )

# No users
# TODO
