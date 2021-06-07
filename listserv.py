""" Listserv Task

Used to handle all interactions with Listserv
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import timeout_action

def add_user_to_listserv(driver: webdriver, user_email: str) -> None:
    """ Adds the user to the CCV and CCV_ANNOUNCE listserv lists
    
    Args:
        your_credentials (ScriptUserCredentials): credentials of the script user for logging into listserv
        user_email (str): the email of the user
    Returns:
        None
    """
    print("Adding user email " + user_email + " to listserv")

    while "Logged in as:" not in driver.page_source:
        # Log in to Listserv manually
        driver.get("https://listserv.brown.edu/cgi-bin/wa?LOGON")
        try:
            print("Waiting for listserv login (times out after 60 seconds)")
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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[@class='message']")))
        message = driver.find_element_by_xpath("//td[@class='message']")
        message_text = message.get_attribute('innerText')
        print(message_text)

    input("\nListserv task completed. Press enter to continue.")