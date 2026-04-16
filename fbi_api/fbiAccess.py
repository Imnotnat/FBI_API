from fbi_api.exceptions import FBIAPIAuthenticationError
from fbi_api.browser import Browser, BrowserDownload

DEBUG = False

def authenticate_user(user) -> bool:
    
    with Browser(headless=not DEBUG) as browser:
        if browser.login(user):
            return True
        else:
            raise FBIAPIAuthenticationError(user)
         
def generateGames_for_user(user, startDate: str, endDate: str):

    with BrowserDownload(headless=not DEBUG) as browser:
        browser.login(user)
        browser.navigate_to_designations()
        browser._apply_date_filters(startDate, endDate)
        browser.provideGames()
        return browser.getGames()