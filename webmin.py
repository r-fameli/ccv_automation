""" Webmin Task

Used to handle all interactions with Webmin
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def add_user_in_webmin(driver: webdriver, batch_string: str, username: str, webmin_access=False) -> None:
    """ Adds the user in webmin using the batch job string 
    
    Args:
        batch_string (str): the string that will be used to create the user
        username(str): the user's AD username
        webmin_access (boolean): True if the program user has access to Webmin (i.e. through Oscar)
    Returns:
        None
    """
    if not webmin_access:
        input("Add user " + username + " to Webmin. Press enter once completed")
    else:
        driver.get("https://nis1:10000/")
        # Wait for login if on the login page
        if "You must enter a username and password" in driver.page_source:
            driver.find_element_by_id("save").click()
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//h3[@class='panel-title']")))
                # EC.presence_of_element_located((By.XPATH("//*[contains(text(), 'System Information')]"))))

        driver.find_element_by_xpath("//a[@href='#system']").click()
        driver.find_element_by_xpath("//a[@href='/useradmin/?xnavigation=1']").click()
        driver.find_element_by_xpath("//a[@href='batch_form.cgi?xnavigation=1']").click()
        
        # Radio button for running by Text in Box
        driver.find_element_by_id("source_2_6056").click()
        text_box = driver.find_element_by_id("text")
        text_box.clear()
        text_box.send_keys(batch_string)
        input("Inputted information into textbox. Press enter in terminal to continue")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='panel-body']/pre")))
        message = driver.find_element_by_xpath("//div[@class='panel-body']/pre").get_attribute('innerText')
        input(message + "Press enter in terminal to continue.")
        
