from enum import Enum


class OTMType(Enum):
    Chronometer = "Chronometreur"
    Marquer = "Marqueur"
    Chronometer24s = "Chronometreur24s"


class AbstractOTM:
     
    def __init__(self, name: str, surname: str, otm_type: OTMType):
        self.name = name
        self.surname = surname
        self.otm_type = otm_type


    def valideOTM(self):
        return False

    def __str__(self):
        return f"OTM : \n    Nom :{self.name},\n Prénom : {self.surname},\n Role : {self.otm_type.value}"

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'otm_type': self.otm_type.value
        }