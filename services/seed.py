from repository.database import create_tables
from repository.nba_repository import load_nba_data_from_api
from repository.player_season_repository import get_player_season


def seed():
    create_tables()
    player_season = get_player_season()
    if not player_season:
        load_nba_data_from_api()



