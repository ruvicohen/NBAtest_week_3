from api.nba_api import get_data_nba_from_api
from repository.player_repository import  create_player, get_player_id_by_name
from repository.player_season_repository import create_player_season
from services.player_service import extract_player_from_nba_data, extract_season_player_from_nba_data
from utils.logics import get_atr, get_points_per_game, get_average_ppg_position
from utils.urls import get_nba_url


def load_nba_data_from_api():
    list_season = ["2022", "2023", "2024"]
    for season in list_season:
        nba_url = get_nba_url(season)
        nba_data_from_api = get_data_nba_from_api(nba_url)
        for player_season_data in nba_data_from_api:
            player_id = get_player_id_by_name(player_season_data["playerName"])
            if not player_id:
                player = extract_player_from_nba_data(player_season_data)
                player_id = create_player(player)
            player_season = extract_season_player_from_nba_data(player_season_data, player_id)
            player_season.atr = get_atr(player_season.assists, player_season.turnovers)
            points_per_game = get_points_per_game(player_season.points, player_season.games)
            average_all = get_average_ppg_position(nba_data_from_api, player_season.position)
            player_season.ppg_ratio = points_per_game / average_all
            create_player_season(player_season)



