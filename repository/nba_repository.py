from toolz import pipe, compose, juxt
from toolz.curried import partial
from api.nba_api import get_data_nba_from_api
from models.player import Player
from repository.database import drop_all_tables, create_tables
from repository.player_repository import  create_player, get_player_id_by_name
from repository.player_season_repository import create_player_season, get_player_season
from services.player_service import extract_player_from_nba_data, extract_season_player_from_nba_data
from utils.logics import get_atr, get_points_per_game, get_average_ppg_per_position, get_ppg_ratio
from utils.urls import get_nba_url

def extract_nba_data_from_api(season):
    return pipe(
        season,
        get_nba_url,
        get_data_nba_from_api
    )

def get_player_id(name: str):
    player_id =  get_player_id_by_name(name)
    if not player_id:
        player_id = create_player(Player(name=name))
    return  player_id

def process_player_data(nba_data):
    return pipe(
        nba_data,
        partial(map, lambda data: { **data, "player_id": get_player_id(data["playerName"]) }),
        partial(map, lambda data: { **data, "atr": get_atr(data["assists"], data["turnovers"]) }),
        partial(map, lambda data:  { **data, "ppg_ratio": get_ppg_ratio(data, nba_data) }),
        list
    )

def load_nba_data_from_api(list_season):
    return pipe(
        list_season,
        partial(map, extract_nba_data_from_api),
        partial(map, process_player_data),
        partial(map, partial(map, create_player_season)),
        partial(map, list),
        list
    )