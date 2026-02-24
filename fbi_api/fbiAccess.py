from fbi_api.exceptions import FBIAPIAuthenticationError
from fbi_api.browser import Browser, BrowserDownload


def authenticate_user(user) -> bool:
    
    with Browser(headless=True) as browser:
        if browser.login(user):
            return True
        else:
            raise FBIAPIAuthenticationError(user)
         
def generateGames_for_user(user, startDate: str, endDate: str):

    with BrowserDownload(headless=False) as browser:
        browser.login(user)
        browser.navigate_to_designations()
        browser._apply_date_filters(startDate, endDate)
        browser.provideGames()
        return browser.getGames()