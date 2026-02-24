from fbi_api.user import FBI_User


def main():
    user = FBI_User("bourachot.natis", "Natilianis2008")
    print("Authenticate :", user.is_authenticated)
    user.authenticate()
    print("Authenticate :", user.is_authenticated)
    user.generateGames("2025-12-31")
    print("Games :", user.games)


if __name__ == "__main__":
    main()