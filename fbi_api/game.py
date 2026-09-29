from typing import Dict, Any

from dataclasses import dataclass, field
from fbi_api.otm import AbstractOTM
from fbi_api.referee import AbstractReferee
from datetime import datetime


@dataclass
class Game :
    game_id: int = None
    date: str = None
    time: str = None
    home_team: str = None
    away_team: str = None
    competition_level: str = None
    venue: str = None
    # Texte après « INDEMNISES PAR : » (ex. « LA FEDERATION ») : qui paie les arbitres
    payer: str = None
    refs: Dict[AbstractReferee, dict[str, int]] = field(default_factory=dict)
    unique_id: str = field(init=False)

    def __post_init__(self):
        self.unique_id = f"{self.game_id}_{self.date}"

    def __str__(self):
        return f"Numéro de rencontre : {self.game_id}, Date: {self.date}, Time: {self.time}, Home Team: {self.home_team}, Away Team: {self.away_team}, Competition Level: {self.competition_level}, Venue: {self.venue}"
    
    def load_from_json(self, data: Dict[str, Any]):
        self.game_id = data.get('game_id')
        self.date = data.get('date')
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
        self.time = data.get('time')
        self.home_team = data.get('home_team')
        self.away_team = data.get('away_team')
        self.competition_level = data.get('competition_level')
        self.venue = data.get('venue')
        self.payer = data.get('payer')
        # Reconstruct refs dictionary from the list of dicts
        self.refs = {}
        for ref_data in data.get('refs', []):
            details = ref_data.pop('details', {})
            # You'll need to recreate the AbstractReferee object from ref_data
            # This is a placeholder - adjust based on your AbstractReferee class
            ref = AbstractReferee(**ref_data)
            self.refs[ref] = details
        self.otms = data.get('otms', [])
        self.otms = [AbstractOTM(**otm_data) for otm_data in data.get('otms', [])]
        self.unique_id = data.get('unique_id', f"{self.game_id}_{self.date}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'game_id': self.game_id,
            'date': self.date,
            'time': self.time,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'competition_level': self.competition_level,
            'venue': self.venue,
            'payer': self.payer,
            'refs': [{**ref.to_dict(), 'details': details} for ref, details in self.refs.items()],
            'otms': [otm.to_dict() for otm in self.otms],
            'unique_id': self.unique_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Game':
        game = cls()
        game.load_from_json(data)
        return game
    
    def __repr__(self):
        return "\n---------Match numéro : " + str(self.game_id) +"--------------------\n" \
        "\nNiveau de compétition : " + self.competition_level + \
        "\nEquipe recevant : " + self.home_team + \
        "\nEquipe visiteur : " + self.away_team + \
        "\nDate : " + str(self.date) + \
        "\nHeure : " + str(self.time) + \
        "\nSalle : " + self.venue + \
        "\nArbitres : " + ",\n ".join([str(ref) for ref in self.refs.keys()]) + \
        "\nOTMs : " + ",\n ".join([str(otm) for otm in self.otms]) + \
        "\n---------------------------------------------\n"  
    