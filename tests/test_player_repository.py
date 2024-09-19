import pytest
from repository.database import create_tables, drop_all_tables
from models.player import Player
from repository.player_repository import create_player, extract_player_from_nba_data, get_player_id_by_name


# Fixture to setup and teardown the database
@pytest.fixture(scope="module")
def setup_database():
    # Setup: Create the necessary tables
    create_tables()

    # Yield control back to the tests
    yield

    # Teardown: Drop all tables after the tests
    drop_all_tables()


@pytest.fixture
def player_data():
    return Player(name="Giannis Antetokounmpo")


# Test the create_player function
def test_create_player(setup_database, player_data):
    new_id = create_player(player_data)

    # Ensure the newly created player has an ID
    assert new_id is not None


# Test the extract_player_from_nba_data function
def test_extract_player_from_nba_data(setup_database):
    nba_data = {"playerName": "LeBron James"}
    player = extract_player_from_nba_data(nba_data)

    # Ensure the extracted player matches the provided data
    assert player.name == "LeBron James"


# Test the get_player_id_by_name function
def test_get_player_id_by_name(setup_database, player_data):
    # First, create a player
    player_name = player_data.name
    create_player(player_data)

    # Retrieve player ID by name
    player_id = get_player_id_by_name(player_name)

    # Ensure the player ID is not None and matches the name
    assert player_id is not None
