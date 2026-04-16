from fbi_api.user import FBI_User
from fbi_api.utils.jsonManager import loadGamesFromJson, saveGamesToJson


def main():
    user = FBI_User("bourachot.natis", "Natilianis2008")
    print("Authenticate :", user.is_authenticated)
    user.authenticate()
    print("Authenticate :", user.is_authenticated)
    user.generateGames("2026-03-28","2026-03-28")
    print("Games :", user.games)

    saveGamesToJson(user.games, "export/games.json")
    '''loadGames = loadGamesFromJson("export/games.json")
    print(loadGames)'''


if __name__ == "__main__":
    main()