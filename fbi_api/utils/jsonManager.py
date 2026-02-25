import json
import os
from datetime import date, time

from fbi_api.game import Game


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, time)):
            return obj.isoformat()
        return super().default(obj)

def saveGamesToJson(games: list[Game], file_path: str) -> None:
    """
    Sauvegarde les données des jeux dans un fichier JSON.

    Args:
        games (list[Game]): Une liste d'objets Game contenant les données des jeux.
        file_path (str): Le chemin du fichier où les données seront sauvegardées.
    """
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump([game.to_dict() for game in games], json_file, cls=DateEncoder, ensure_ascii=False, indent=4)

def loadGamesFromJson(file_path: str) -> list[Game]:
    """
    Charge les données des jeux à partir d'un fichier JSON.

    Args:
        file_path (str): Le chemin du fichier JSON à partir duquel les données seront chargées.

    Returns:
        list[Game]: Une liste d'objets Game contenant les données des jeux.
    """
    with open(file_path, 'r', encoding='utf-8') as json_file:
        games = json.load(json_file)
    return [Game.from_dict(game_dict) for game_dict in games]