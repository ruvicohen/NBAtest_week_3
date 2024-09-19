from api.nba_api import get_data_nba_from_api
from repository.database import drop_all_tables, create_tables
from repository.player_repository import extract_player_from_nba_data, create_player, get_player_id_by_name
from repository.player_season_repository import extract_season_player_from_nba_data, create_player_season, \
    get_player_season
from utils.logics import get_atr, get_points_per_game
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
            average_all = get_average_per_position(player_season_data, player_season.position)
            player_season.ppg_ratio = points_per_game / average_all
            create_player_season(player_season)

def get_average_per_position(nba_data, position):
    filter_list = list(filter(lambda player: player['position'] == position, nba_data))
    sum_games = sum(list(map(lambda player: player['games'], filter_list)))
    sum_points = sum(list(map(lambda player: player['points'], filter_list)))
    return sum_points / sum_games

drop_all_tables()
create_tables()
load_nba_data_from_api()
print(get_player_season())