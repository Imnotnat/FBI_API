from typing import Dict, Optional, Any

from dataclasses import dataclass, field
import re
import pdfplumber
from datetime import datetime
from fbi_api.referee import AbstractReferee


@dataclass
class Game :
    game_id: int = None
    date: str = None
    time: str = None
    home_team: str = None
    away_team: str = None
    competition_level: str = None
    venue: str = None
    refs: list[AbstractReferee] = field(default_factory=list)
    ref1_pay: float = 0.0
    ref2_pay: float = 0.0
    ref3_pay: float = 0.0
    unique_id: str = field(init=False)

    def __post_init__(self):
        self.unique_id = f"{self.game_id}_{self.date}"

    def __str__(self):
        return f"Numéro de rencontre : {self.game_id}, Date: {self.date}, Time: {self.time}, Home Team: {self.home_team}, Away Team: {self.away_team}, Competition Level: {self.competition_level}, Venue: {self.venue}"
    

def _extract_data_from_pdf(pdf_path: str) -> Optional[Dict[str, Any]]:
    """
    Extract match data from PDF using regex on the text content.
    """
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        if not text:
            return None

        data = {
            'unique_id' : None,
            'external_id': None,
            'date': None,
            'time': None,
            'home_team': None,
            'away_team': None,
            'venue': None,
            'referee_1_name': None,
            'referee_1_pay' : None,
            'referee_2_name': None,
            'referee_2_pay': None,
            'referee_3_name': None,
            'referee_3_pay': None,
            'competition_level': None
        }

        # 1. Date, Heure, ID
        date_match = re.search(r"DATE\s*:\s*(\d{2}/\d{2}/\d{4})", text)
        time_match = re.search(r"HEURE\s*:\s*(\d{2}:\d{2})", text)
        id_match = re.search(r"N°\s*RENCONTRE\s*:\s*(\d+)", text)



        if date_match:
            data['date'] = datetime.strptime(date_match.group(1), "%d/%m/%Y").date()
        if time_match:
            data['time'] = datetime.strptime(time_match.group(1), "%H:%M").time()
        if id_match:
            data['external_id'] = f"FBI_{id_match.group(1)}"
        if id_match and date_match:
            data['unique_id'] = f"FBI_{id_match.group(1)}_{date_match.group(1)}"
        elif data['date'] and data['time']:
            data['external_id'] = f"FBI_{data['date']}_{data['time']}".replace('-', '')

        # 2. Compétition
        comp_match = re.search(r"COMPETITION\s*:\s*(.+)", text)
        if comp_match:
            data['competition_level'] = comp_match.group(1).strip()

        # 3. Equipes
        home_match = re.search(r"RECEVANT\s*:\s*(.+?)(?:\n|$)", text)
        away_match = re.search(r"VISITEUR\s*:\s*(.+?)(?:\n|$)", text)

        if home_match:
            data['home_team'] = home_match.group(1).strip().replace(" - ", " ").strip()
        if away_match:
            data['away_team'] = away_match.group(1).strip().replace(" - ", " ").strip()

        #TODO
        # 4. Salle (Venue)
        venue_match = re.search(r"Adresse de la salle.*?(?:\n.*?)*?(\d{5}\s+[A-Z\-\s]+)", text, re.DOTALL)
        if venue_match:
            data['venue'] = venue_match.group(1).strip()
        else:
            zip_match = re.search(r"\b\d{5}\s+[A-Z\-\s]{3,}\b", text)
            if zip_match:
                data['venue'] = zip_match.group(0).strip()

        # 5. Arbitres
        refs = re.findall(r"Arbitre\s*:\s*([^\(]+)", text)

        clean_refs = [r.strip() for r in refs if r.strip()]

        indemnite_match = re.findall(r"Indemnité\s*:\s*(\d+\.\d{2})\s*€", text)

        clean_indem = [r.strip() for r in indemnite_match if r.strip()]


        km_match = re.findall(r"Nbre de kms aller\s*:\s*(\d+\. 00)", text)
        clean_km = [km.strip() for km in km_match if km.strip()]

        if len(clean_refs) > 0:
            data['referee_1_name'] = clean_refs[0]
            data['referee_1_pay'] = clean_indem[0]
        if len(clean_refs) > 1:
            data['referee_2_name'] = clean_refs[1]
            data['referee_2_pay'] = clean_indem[1]
        if len(clean_refs) > 2:
            data['referee_3_name'] = clean_refs[2]
            data['referee_3_pay'] = clean_indem[2]

        # Validation minimale et LOG VISUEL
        if data['date'] and data['home_team']:
            # C'est ici que l'info s'affiche dans ta console
            print(f"✅ {data['home_team']} vs {data['away_team']} ({data['date']})") # <--- AJOUT
            return data

        return None

    except Exception as e:
        #TODO logger.error(f"Error parsing PDF content: {e}")
        return None