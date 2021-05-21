""" Deskpro Interactions

Used to handle all interactions with Deskpro
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from user_data import User

def generate_user_notification_html(user_info: User) -> None:
    """ Generates a message in HTML to send back to the user in Deskpro to notify them that their account has been created

    Args:
        user_info (User): the information of the user that stores their name and username
    Returns:
        None: prints an HTML string that can be input using Deskpro's html feature
    """
    print(""" 

    NOTIFY USER
    ==============================

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
     <p></p>

     ==============================
    """.format(first_name = user_info.first_name, username = user_info.username))
    input('''Copy the above message (Ctrl+Insert or Ctrl+Shift+C in Linux-based terminals). 
    In Deskpro, select the option to insert using HTML and paste the message in. Then turn off the HTML setting.
     Press enter once you have added your name and sent the message.''')

def retrieve_from_deskpro(driver, ticket_id):
    driver.get("https://ithelp.brown.edu/agent/")

    # ensure that only one ticket is open
    tabs_open = driver.find_elements_by_xpath("//a[@class='ng-binding']").length
    if tabs_open != 0:
        # Right click the tabs bar and close all tabs
        print("Closing Deskpro tabs")
        tabs_bar = driver.find_element_by_xpath("//div[@class='deskproTabListInner ng-isolate-scope']")
        ActionChains(driver).context_click(tabs_bar)
        driver.find_element_by_xpath("//a[@ng-click='closeAll()']").click()
    
    ticket_message = driver.find_elements_by_xpath("//div[@class='body-text-message unreset']")[-1]

# def insert_into_deskpro(user_notification: str, ticket_num: int) -> None:
#     """ Inserts the user notification into Deskpro for the appropriate ticket

#     Args:
#         user_notification (str): the notification that will be sent to the user
#         ticket_num (int): the number of the ticket to insert into
#     """

     # def scrape_from_deskpro() -> list:
#     print("")
#     # TODO
#     # find last element where xpath is //div[@class='body-text-message unreset'] (ENSURE THAT ONLY ONE TAB IS OPEN IN DESKPRO)
#     # TO CLOSE ALL TABS:
#     # right click in //div[@class='deskproTabListInner ng-isolate-scope']
#     # click on //li[@ng-show='showCloseAll()']
#     # 
