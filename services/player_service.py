from models.player import Player
from models.player_season_status import PlayerSeasonStatus

def extract_player_from_nba_data(nba_data) -> Player:
    return Player(
        name=nba_data["playerName"]
    )

def extract_season_player_from_nba_data(nba_data):
    return PlayerSeasonStatus(
        player_id=nba_data["player_id"],
        team=nba_data["team"],
        position=nba_data["position"],
        seasons=nba_data["season"],
        points=nba_data["points"],
        games=nba_data["games"],
        atr=nba_data["atr"],
        assists=nba_data["assists"],
        turnovers=nba_data["turnovers"],
        two_percent=nba_data["twoPercent"],
        three_percent=nba_data["threePercent"]

    )