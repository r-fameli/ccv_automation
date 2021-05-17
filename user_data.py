class User:
    """ Stores a user's information """
    def __init__(self, first_name, username, email):
        self.first_name = first_name
        self.username = username
        self.email = email

class ProgramSettings:
    """ Stores settings for the program, as specified by the user """
    def __init__(self, webmin_access):
        self.webmin_access = webmin_access