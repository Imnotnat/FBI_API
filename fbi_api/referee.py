class AbstractReferee:

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    def valideRef(self):
        return False

    def __str__(self):
        return f"Arbitre : \n    Nom :{self.name},\n Prénom : {self.surname}"
    
class Referee(AbstractReferee):

    def __init__(self, name: str, surname: str):
        super().__init__(name, surname)
        self.games = []

    def valideRef(self):
        return True
