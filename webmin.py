""" Webmin Task

Used to handle all interactions with Webmin
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from user_data import ScriptUserCredentials


def add_user_in_webmin(batch_string_file: str, username: str) -> None:
    """ Adds the user in webmin using the batch job string 
    
    Args:
        batch_string_file (str): the string that will be used to create the user
        username(str): the user's AD username
    Returns:
        None
    """
    input("Add user " + username + " to Webmin. Press enter once completed")
