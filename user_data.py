class ScriptUserCredentials:
    """ Holds the information of the user using the script """
    def __init__(self, username, email, brown_password, listserv_password):
        """ Creates a new instance of ScriptUserInfo """
        self.username = username
        self.email = email
        self.brown_password = brown_password
        self.listserv_password = listserv_password

    def update_listserv_password(self, new_listserv_password):
        """ Updates the listserv password stored """
        self.listserv_password = new_listserv_password

    def update_brown_password(self, new_brown_password):
        """ Updates the Brown password stored """
        self.brown_password = new_brown_password

class User:
    """ Stores a user's information """
    def __init__(self, first_name, username, email):
        self.first_name = first_name
        self.username = username
        self.email = email
