'''class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"
    
class FBI_User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __str__(self):
        return f"FBI_User(username='{self.username}', password='{'*' * len(self.password)}')"'''
##########################################################################################

from fbi_api.exceptions import FBIAPIAuthenticationError
from fbi_api.fbiAccess import authenticate_user, generateGames_for_user


class FBI_User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.games = []
        self.is_authenticated = False

    def generateGames(self, startDate: str = "2000-1-1", endDate: str = "2100-1-1"):
        if not self.is_authenticated:
            raise FBIAPIAuthenticationError(self)

        print(f"Generating games for user '{self.username}' between {startDate} and {endDate}...")
        self.games = generateGames_for_user(self, startDate, endDate)
        
    def getGamesByDate(self, startDate: str= "2000-1-1", endDate: str =  "2100-1-1"):
        if not self.games:
            self.generateGames(startDate, endDate)
        return [game for game in self.games if startDate <= game["date"] <= (endDate or "2100-1-1")]
    
    def getGames(self):
        if not self.games:
            self.generateGames()
        return self.games
        
    def __str__(self):
        return f"FBI_User(username='{self.username}', password='{'*' * len(self.password)}')"
    
    def authenticate(self):
        self.is_authenticated = authenticate_user(self)