""" Deskpro Interactions

Used to handle all interactions with Deskpro
"""

from user_data import User

def generate_user_notification_html(user_info: User) -> None:
    """ Generates a message in HTML to send back to the user in Deskpro to notify them that their account has been created

    Args:
        user_info (UserInfo): the information of the user that stores their name and username
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


     # def scrape_from_deskpro() -> list:
#     print("")
#     # TODO
#     # find last element where xpath is //div[@class='body-text-message unreset'] (ENSURE THAT ONLY ONE TAB IS OPEN IN DESKPRO)
#     # TO CLOSE ALL TABS:
#     # right click in //div[@class='deskproTabListInner ng-isolate-scope']
#     # click on //li[@ng-show='showCloseAll()']
#     # 
