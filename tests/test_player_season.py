import pytest
from models.player import Player
from repository.database import create_tables, drop_all_tables
from repository.player_repository import create_player
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
    drop_all_tables()


# Fixture for creating a PlayerSeasonStatus object
@pytest.fixture
def player_season():
    # Create a new player to associate with the season
    player = Player(name="Kobe Bryant")
    player_id = create_player(player)

    # Return a PlayerSeasonStatus object for testing
    return {
        "player_id": player_id,
        "team": "Lakers",
        "position": "SG",
        "season": 2024,
        "points": 252,
        "games": 56,
        "assists": 19,
        "turnovers": 20,
        "twoPercent": 0.519,
        "threePercent": 0.408,
        "atr": 2.5,
        "ppg_ratio": 1.1
    }

# Test the create_player_season function
def test_create_player_season(setup_database, player_season):
    new_id = create_player_season(player_season)
    assert new_id is not None

# Test the get_player_season function
def test_get_player_season(setup_database, player_season):
    create_player_season(player_season)  # Add a player season to test retrieval
    result = get_player_season()
    assert len(result) > 0
    assert any(ps['player_id'] == player_season["player_id"] for ps in result)

# Test the get_players_by_position_and_season function
def test_get_players_by_position_and_season(setup_database, player_season):
    create_player_season(player_season)  # Add a player season for this position and season
    position = player_season["position"]
    season = player_season["season"]

    result = get_players_by_position_and_season(position, season)
    assert len(result) > 0
    assert all(r['position'] == position for r in result)
    assert all(r['seasons'] == season for r in result)

# Test the get_by_season function
def test_get_by_season(setup_database, player_season):
    create_player_season(player_season)  # Add a player season for the test season
    season = player_season["season"]

    result = get_by_season(season)
    assert len(result) > 0
    assert all(r['seasons'] == season for r in result)

# Test the get_by_player_id function
def test_get_by_player_id(setup_database, player_season):
    player_id = player_season["player_id"]
    create_player_season(player_season)  # Add a player season for the player

    result = get_by_player_id(player_id)
    assert len(result) > 0
    assert all(r['player_id'] == player_id for r in result)

# Test the get_players_by_team_id function
# def test_get_players_by_team_id(setup_database, player_season):
#     team_id = 1  # Assuming team_id is known
#     create_player_season(player_season)  # Add a player season associated with the team
#
#     result = get_players_by_team_id(team_id)
#     assert len(result) > 0
#     assert all(r['team_name'] == player_season["team"] for r in result)