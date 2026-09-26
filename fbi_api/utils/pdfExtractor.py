import re
from typing import Any, Dict, Optional
import pdfplumber
from fbi_api.game import Game
from datetime import datetime
from fbi_api.otm import AbstractOTM, OTMType
from fbi_api.referee import AbstractReferee

def _extract_venue(text: str) -> Optional[str]:
    """
    Extract the full venue address from the PDF text.

    The line looks like:
    "Adresse de la salle :SALLE OMNISPORTS 67 Av. de Provence 06130 GRASSE (Tél:0493401849)"
    The phone part may be missing or truncated (e.g. "(Tél:06").
    """
    venue_match = re.search(r"Adresse de la salle\s*:\s*([^\n]+)", text)
    if venue_match:
        venue = re.sub(r"\s*\(T[ée]l\b.*$", "", venue_match.group(1)).strip()
        if venue:
            return venue

    zip_match = re.search(r"\b\d{5}[ \t]+[A-Z][A-Z\- \t]{2,}\b", text)
    if zip_match:
        return zip_match.group(0).strip()
    return None


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

        game = Game()

        # 1. Date, Heure, ID
        date_match = re.search(r"DATE\s*:\s*(\d{2}/\d{2}/\d{4})", text)
        time_match = re.search(r"HEURE\s*:\s*(\d{2}:\d{2})", text)
        id_match = re.search(r"N°\s*RENCONTRE\s*:\s*(\d+)", text)



        if date_match:
            game.date = datetime.strptime(date_match.group(1), "%d/%m/%Y").date()
        if time_match:
            game.time = datetime.strptime(time_match.group(1), "%H:%M").time()
        if id_match:
            game.game_id = int(id_match.group(1))
        if id_match and date_match:
            game.unique_id = f"FBI_{id_match.group(1)}_{date_match.group(1)}"
        elif game.date and game.time:
            game.unique_id = f"FBI_{game.date}_{game.time}".replace('-', '')

        # 2. Compétition
        comp_match = re.search(r"COMPETITION\s*:\s*(.+)", text)
        if comp_match:
            game.competition_level = comp_match.group(1).strip()

        # 3. Equipes
        home_match = re.search(r"RECEVANT\s*:\s*(.+?)(?:\n|$)", text)
        away_match = re.search(r"VISITEUR\s*:\s*(.+?)(?:\n|$)", text)

        if home_match:
            game.home_team = home_match.group(1).strip().replace(" - ", " ").strip()
        if away_match:
            game.away_team = away_match.group(1).strip().replace(" - ", " ").strip()

        # 4. Salle (Venue)
        game.venue = _extract_venue(text)

        # 5. Arbitres
        refs = re.findall(r"Arbitre\s*:\s*([^\(]+)", text)

        clean_refs_name = [r.strip().split(" ", 1) for r in refs if r.strip()]

        indemnite_match = re.findall(r"Indemnité\s*:\s*(\d+\.\d{2})\s*€", text)

        clean_indem = [r.strip() for r in indemnite_match if r.strip()]

        km_match = re.findall(r"Nbre de kms aller\s*:\s*(\d+\.\d{2})", text)
    
        clean_km = [km.strip() for km in km_match if km.strip()]

        if len(clean_refs_name) > 0:
            game.refs[AbstractReferee(clean_refs_name[0][0], clean_refs_name[0][1])] = {
                'pay': float(clean_indem[0]) if clean_indem else 0.0,
                'km': float(clean_km[0]) if clean_km else 0.0
            }
        if len(clean_refs_name) > 1:
            game.refs[AbstractReferee(clean_refs_name[1][0], clean_refs_name[1][1])] = {
                'pay': float(clean_indem[1]) if len(clean_indem) > 1 else 0.0,
                'km': float(clean_km[1]) if len(clean_km) > 1 else 0.0
            }
        if len(clean_refs_name) > 2:
            game.refs[AbstractReferee(clean_refs_name[2][0], clean_refs_name[2][1])] = {
                'pay': float(clean_indem[2]) if len(clean_indem) > 2 else 0.0,
                'km': float(clean_km[2]) if len(clean_km) > 2 else 0.0
            }

        #OTM
        if not hasattr(game, 'otms'):
            game.otms = []

        marquer = re.search(r"Marqueur\s*:\s*([^\(]+)", text)
        if marquer:
            marquer_name = marquer.group(1).strip().split(" ", 1)
            if len(marquer_name) == 2:
                game.otms.append(AbstractOTM(marquer_name[0], marquer_name[1], OTMType.Marquer))
        chronometreur = re.search(r"Chronometreur\s*:\s*([^\(]+)", text)
        if chronometreur:
            chrono_name = chronometreur.group(1).strip().split(" ", 1)
            if len(chrono_name) == 2:
                game.otms.append(AbstractOTM(chrono_name[0], chrono_name[1], OTMType.Chronometer))
        chrono24s = re.search(r"Chronométreur tirs\s*:\s*([^\(]+)", text)
        if chrono24s:
            chrono24s_name = chrono24s.group(1).strip().split(" ", 1)
            if len(chrono24s_name) == 2:
                game.otms.append(AbstractOTM(chrono24s_name[0], chrono24s_name[1], OTMType.Chronometer24s))

        # Validation minimale et LOG VISUEL
        if game.date and game.home_team:
            # C'est ici que l'info s'affiche dans ta console
            print(f"✅ {game.home_team} vs {game.away_team} ({game.date})") # <--- AJOUT
            return game

        return None

    except Exception as e:
        #TODO logger.error(f"Error parsing PDF content: {e}")
        print(f"Error parsing PDF content: {e}")
        return None