import pytest
from repository.database import create_tables, drop_all_tables
from models.player_season_status import PlayerSeasonStatus
from repository.nba_repository import load_nba_data_from_api
from repository.player_season_repository import create_player_season, extract_season_player_from_nba_data, get_player_season, \
    get_by_season, get_by_player_id


# This fixture will set up and tear down the database
@pytest.fixture(scope="module")
def setup_database():
    # Setup: Create the tables and load the data
    create_tables()
    load_nba_data_from_api()

    # Yield control back to the tests
    yield

    # Teardown: Drop the tables after the tests
    drop_all_tables()


@pytest.fixture
def player_season():
    return PlayerSeasonStatus(
        player_id="greenaj01",
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


# Test the create_player_season function
def test_create_player_season(setup_database, player_season):
    new_id = create_player_season(player_season)

    # Ensure that the newly created player season has an ID
    assert new_id is not None


# Test the extract_season_player_from_nba_data function
def test_extract_season_player_from_nba_data(setup_database):
    nba_data = {
        "team": "MIL",
        "position": "SG",
        "season": 2024,
        "points": 252,
        "games": 56,
        "twoPercent": 0.519,
        "threePercent": 0.408,
    }
    player_id = "greenaj01"

    player_season = extract_season_player_from_nba_data(nba_data, player_id)

    # Ensure the extracted player season status matches the provided data
    assert player_season.player_id == player_id
    assert player_season.team == "MIL"
    assert player_season.position == "SG"
    assert player_season.seasons == 2024
    assert player_season.points == 252
    assert player_season.games == 56
    assert player_season.two_percent == 0.519
    assert player_season.three_percent == 0.408


# Test the get_player_season function
def test_get_player_season(setup_database):
    result = get_player_season()

    # Ensure we get some results from the database
    assert len(result) > 0


# Test the get_by_season function
def test_get_by_season(setup_database):
    season = 2024
    result = get_by_season(season)

    # Ensure the result matches the expected season
    assert all(r['seasons'] == season for r in result)


# Test the get_by_player_id function
def test_get_by_player_id(setup_database):
    player_id = "greenaj01"
    result = get_by_player_id(player_id)

    # Ensure the result contains the correct player_id
    assert all(r['player_id'] == player_id for r in result)
