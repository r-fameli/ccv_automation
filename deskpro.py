""" Deskpro Interactions

Used to handle all interactions with Deskpro
"""
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager

from utils import timeout_action, wait_and_click_by_xpath, wait_and_return_element_by_xpath, wait_and_return_elements_by_xpath
from user_data import User

# ticket_message = driver.find_elements_by_xpath("//div[@class='body-text-message unreset']")[-1]

    # def scrape_from_deskpro() -> list:
#     print("")
#     # TODO
#     # find last element where xpath is //div[@class='body-text-message unreset'] (ENSURE THAT ONLY ONE TAB IS OPEN IN DESKPRO)
#     # TO CLOSE ALL TABS:
#     # right click in //div[@class='deskproTabListInner ng-isolate-scope']
#     # click on //li[@ng-show='showCloseAll()']
#     #

def print_deskpro_notification_in_terminal(user_info: User) -> None:
    """ Print a message in HTML to send back to the user in Deskpro to notify them that their account has been created

    Args:
        user_info (User): the information of the user that stores their name and username
    Returns:
        None
    """
    print("NOTIFY USER")
    print("==============================")
    print("")
    print(generate_user_notification_html(user_info))
    print("")
    print("==============================")
    input('''Copy the above message (Ctrl+Insert or Ctrl+Shift+C in Linux-based terminals). 
    In Deskpro, select the option to insert using HTML and paste the message in. Then turn off the HTML setting.
     Press enter once you have added your name and sent the message.''')


        

def insert_notification_into_deskpro(driver: webdriver, ticket_id: int, user_info: User):
    """ Inserts the given notification HTML into a ticket

    Args:
        driver (webdriver): the browser driver in use
        ticket_id (int): the id of the ticket
        user_info (User): the user that the account is being created for
    Returns:
        None
    """
    user_notification_html = generate_user_notification_html(user_info)

    if clear_tabs_and_find_ticket(driver, ticket_id):
        # Turn on the setting for inserting as HTML
        print("Inserting into Deskpro")
        html_button_xpath = "//a[@title='HTML']"
        wait_and_click_by_xpath(driver, html_button_xpath)
        message_box = driver.find_element_by_xpath("//textarea[@name='message']")
        message_box.clear()
        message_box.send_keys(user_notification_html)
        wait_and_click_by_xpath(driver, html_button_xpath)
        print("Email notification has been pasted into Deskpro for ticket " + str(ticket_id))
    else:
        print("Could not automate insertion into Deskpro")


def generate_user_notification_html(user_info: User) -> str:
    """ Generates a message in HTML to send back to the user in Deskpro to notify them that their account has been created

    Args:
        user_info (User): the information of the user that stores their name and username
    Returns:
        str: an HTML string that can be input using Deskpro's html feature
    """
    return """ 
    <p></p><p><span></span></p><p></p><p></p><p></p><p>Hi {first_name},</p><p><br></p><p>Your Oscar account was created -
     you should be able to login with the same credentials as used for other Brown services. Let us know if you encounter any issues. 
     To access via terminal/command line: </p><p></p><pre class="dp-pre">ssh {username}@ssh.ccv.brown.edu</pre><p>
     Documentation for new users can be found at this link:&nbsp;</span><a href="https://docs.ccv.brown.edu/oscar/getting-started">
     <span>https://docs.ccv.brown.edu/oscar/getting-started</span></a><span>.</span></span></p><p><span><span>
     We offer workshops on using Oscar, upcoming sessions can be found at this link:&nbsp;</span><a href="https://events.brown.edu/ccv/view/all">
     <span>https://events.brown.edu/ccv/view/all</span></a></span></p><p><span><span><strong>Note: </strong>
     This account and all CCV systems fall under the Computing Policy for Brown University. You can review this policy at </span>
     <a href="https://it.brown.edu/computing-policies"><span>https://it.brown.edu/computing-policies</span></a></span></p><p><br></p>
     <p>Thank you,</p>
     <p><br></p>
     <p></p>""".format(first_name=user_info.first_name, username=user_info.username)

def clear_tabs_and_find_ticket(driver: webdriver, ticket_id: int):
    """ Closes all Deskpro tabs and opens the ticket with the given id

    Args:
        driver (webdriver): the browser driver in use
        ticket_id (int): the ID of the ticket
    Returns:
        bool: False if ticket could not be found, else True
    """
    deskpro_login(driver)

    # Go to your open tickets
    WebDriverWait(driver, 15).until_not(EC.presence_of_element_located((By.ID, "dp_loading")))
    wait_and_click_by_xpath(driver, "//div[@class='item']/h3[text()='Open Tickets - Me']")
    # Ensure that no ticket tabs are open
    tabs_open = len(driver.find_elements_by_xpath("//a[@class='ng-binding']"))
    if tabs_open != 0:
        # Right click the tabs bar and close all tabs
        print("Closing Deskpro tabs")
        tabs_bar = driver.find_element_by_xpath("//div[@class='deskproTabListInner ng-isolate-scope']")
        ActionChains(driver).context_click(tabs_bar)
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@ng-click='closeAll()']")))
            driver.find_element_by_xpath("//a[@ng-click='closeAll()']").click()
            WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//a[@class='ng-binding']")))
        except:
            pass
        
    
    try:
        # Find the ticket in the list
        print("Opening ticket " + str(ticket_id))
        ticket_xpath = "//span[@class='obj-id' and text()='#" + str(ticket_id) + "']"
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ticket_xpath)))
        ticket_id_indicator = driver.find_element_by_xpath(ticket_xpath)
    except:
        print("Could not find ticket with id " + str(ticket_id))
        return False

    WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.ID, "dp_loading")))
    ticket_id_indicator.click()
    return True
    


def deskpro_login(driver: webdriver):
    """ Waits for the user to log into Deskpro

    Args:
        driver (webdriver): the browser driver in use
    Returns:
        None
    """
    driver.get("https://ithelp.brown.edu/agent/")

    # Wait for log in
    while "Deskpro Agent Interface" not in driver.title:
        # Log in to Grouper manually
        print("Waiting for manual Deskpro login (times out after 60 seconds)")
        try:
            WebDriverWait(driver, 60).until_not(
                EC.title_contains("Brown University"))
            WebDriverWait(driver, 30).until(
                EC.title_contains("Deskpro Agent Interface"))
            break
        except TimeoutException as ex:
            timeout_action(driver)
    WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, "//h1[text()='Loading Interface']")))
    print("Deskpro loaded")


def retrieve_account_string_from_deskpro(driver: webdriver, ticket_id: int) -> str:
    """ Opens Deskpro and finds the given ticket. Scrapes the last message to receive the relevant account string.

    Args:
        driver (webdriver): the browser driver in use
        ticket_id (int): the ID of the ticket
    Returns:
        str: an account string of the form <date>,<brown_id>,<full_name>,<email>,<pi_email>,<phone>
    """
    if clear_tabs_and_find_ticket(driver, ticket_id):
        # Get the last message
        first_message_element = wait_and_return_element_by_xpath(driver, "(//div[@class='body-text-message unreset'])[last()]")
        first_message = first_message_element.get_attribute('innerText')
        account_str = re.search(r"\d+/\d+/\d+.*", first_message).group()
        print("Found account string " + account_str)
        return account_str
    else:
        print("Could not retrieve user information automatically from Deskpro.")
        return ""




# def test_deskpro():
#     test_user = User("Riki", "rfameli1", "riki_fameli@brown.edu")
#     insert_into_deskpro(
#         webdriver.Firefox(executable_path=GeckoDriverManager(
#             cache_valid_range=1).install()),
#         generate_user_notification_html(test_user),
#          245422
#     )
#
# insert_notification_into_deskpro( 
#     webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=1).install()), 
#     245977, 
#     User("Jade", "jkemp3", "niloufar_razmi@brown.edu")
#     )
# test_deskpro()



