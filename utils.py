import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def confirm_action(message: str) -> bool:
    """ Presents a simple confirmation message and returns a boolean based on the yes/no value inputted

    Args:
        message (str): the message to be presented to the user
    Returns:
        bool: True if the user inputs 'y' or 'yes'. False if user inputs 'n' or 'no'.
    """
    response = prompt_to_choose_option(message, ["yes", "y", "no", "n"])
    return (response == "y" or response == "yes")

def timeout_action(driver_in_use: webdriver) -> None:
    """ Prints a timeout statement to the user and closes the driver and program 
    
    Args:
        driver_in_use (WebDriver): the driver that is currently being used
    Returns:
        None
    """
    print("Action failed to complete in time, closing driver")
    driver_in_use.close()
    sys.exit(1)

def prompt_to_choose_option(prompt: str, acceptable_inputs: list, case_sensitive = False) -> str:
    """ Prompts the user and will only accept inputs listed in acceptable_inputs

    Args:
        prompt (str): the message to display to the user initially
        acceptable_inputs (list): the list of acceptable inputs
        case_sensitive(bool): optional arg that specifies whether arguments are case sensitive
    Returns:
        str: the item from acceptable_inputs the user inputted
    Throws:
        Exception if acceptable_inputs is empty
    """
    if not acceptable_inputs:
        raise Exception("prompt_to_choose_option requires a non-empty list of acceptable inputs")

    if not case_sensitive:
        acceptable_inputs = list(map(lambda choice: choice.casefold(), acceptable_inputs))

    user_input = input(prompt)
    checking_inputs = True
    while checking_inputs:
        if not case_sensitive:
            user_input = user_input.casefold()

        if user_input.strip() in acceptable_inputs:
            return user_input

        # Format the string to present to the user if input is invalid
        choices_string = ""
        number_of_choices = len(acceptable_inputs)
        if number_of_choices == 1:
            choices_string = "'" + acceptable_inputs[0] + "'" + " is the only choice."
        elif number_of_choices == 2:
            choices_string = "Choices are '" + acceptable_inputs[0] + "' or '" + acceptable_inputs[1] + "'."
        else:
            choices_string = "Choices are "
            for i in range(0, number_of_choices - 1):
                choices_string += "'" + acceptable_inputs[i] + "', "
            choices_string += "or '" + acceptable_inputs[-1] + "'."

        # Ask the user to re-input
        user_input = input(
            user_input + " is not an acceptable input. " + choices_string + " (Ignore quotation marks): ")
            

def wait_and_click_by_xpath(driver: webdriver, xpath: str, timeout=15) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.find_element_by_xpath(xpath).click()
    except TimeoutException as ex:
        print("ERROR: " + str(ex))
        timeout_action(driver)

def wait_and_return_element_by_xpath(driver: webdriver, xpath: str, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)
    except TimeoutException as ex:
        print("ERROR: " + str(ex))
        timeout_action(driver)

def wait_and_return_elements_by_xpath(driver: webdriver, xpath: str, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_elements_by_xpath(xpath)
    except TimeoutException as ex:
        print("ERROR: " + str(ex))
        timeout_action(driver)

# prompt_to_choose_option("one", ["one"])
# prompt_to_choose_option("two", ["one", "two"])
# prompt_to_choose_option("three", ["one", "two", "three"])