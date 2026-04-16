from enum import Enum


class OTMType(Enum):
    Chronometer = "Chronometreur"
    Marquer = "Marqueur"
    Chronometer24s = "Chronometreur24s"
    
    @classmethod
    def from_string(cls, value: str):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Invalid OTMType value: {value}")


class AbstractOTM:
     
    def __init__(self, name: str, surname: str, otm_type: OTMType):
        self.name = name
        self.surname = surname
        self.otm_type = otm_type if isinstance(otm_type, OTMType) else OTMType.from_string(otm_type)


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
    
    def isMarqueur(self):
        return self.otm_type == OTMType.Marquer
    
    def isChronometer(self):
        return self.otm_type == OTMType.Chronometer
    
    def isChronometer24s(self):
        return self.otm_type == OTMType.Chronometer24s
    
