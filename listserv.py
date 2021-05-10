""" Listserv Task

Used to handle all interactions with Listserv
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from user_data import ScriptUserCredentials
from utils import timeout_action

def add_user_to_listserv(driver: webdriver, your_credentials: ScriptUserCredentials, user_email: str) -> None:
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