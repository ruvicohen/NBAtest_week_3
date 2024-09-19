import pytest

from models.player import Player
from repository.database import create_tables, drop_all_tables
from models.player_season_status import PlayerSeasonStatus
from repository.player_repository import create_player, delete_player
from repository.player_season_repository import (
    create_player_season,
    get_player_season,
    get_players_by_position_and_season,
    get_by_season,
    get_by_player_id
)

# Fixture for setting up the database and tearing it down
@pytest.fixture(scope="module")
def setup_database():
    # Setup: Create the tables
    create_tables()
    yield
    # Teardown: Drop the tables after the tests
    #drop_all_tables()

# Fixture for creating a PlayerSeasonStatus object
@pytest.fixture
def player_season():
    player = Player(name="kobi")
    player_id = create_player(player)
    return PlayerSeasonStatus(
        player_id=player_id,
        team="MIL",
        position="SG",
        seasons=2024,
        points=252,
        games=56,
        assists=19,
        turnovers=20,
        two_percent=0.519,
        three_percent=0.408,
        atr=2.5,
        ppg_ratio=1.1
    )
    #delete_player(player_id)

# Test the create_player_season function
def test_create_player_season(setup_database, player_season):
    new_id = create_player_season(player_season)
    assert new_id is not None


# Test the get_player_season function
def test_get_player_season(setup_database):
    result = get_player_season()
    assert len(result) > 0

# Test the get_players_by_position_and_season function
def test_get_players_by_position_and_season(setup_database):
    position = "SG"
    season = 2024
    result = get_players_by_position_and_season(position, season)
    assert all(r['position'] == position for r in result)
    assert all(r['seasons'] == season for r in result)

# Test the get_by_season function
def test_get_by_season(setup_database):
    season = 2024
    result = get_by_season(season)
    assert len(result) > 0
    assert all(r['seasons'] == season for r in result)

# Test the get_by_player_id function
def test_get_by_player_id(setup_database):
    player_id = 1
    result = get_by_player_id(player_id)
    assert len(result) > 0
    assert all(r['player_id'] == player_id for r in result)




