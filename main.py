from fbi_api.user import FBI_User
from fbi_api.utils.jsonManager import saveGamesToJson


def main():
    user = FBI_User("bourachot.natis", "Natilianis2008")
    print("Authenticate :", user.is_authenticated)
    user.authenticate()
    print("Authenticate :", user.is_authenticated)
    user.generateGames("2026-2-28","2026-2-28")
    print("Games :", user.games)

    saveGamesToJson(user.games, "export/games.json")


if __name__ == "__main__":
    main()