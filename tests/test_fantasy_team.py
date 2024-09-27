import pytest
from repository.database import create_tables, drop_all_tables
from repository.fantasy_team_repository import create_team, update_team, delete_team, get_team_name_by_id


# Fixture for setting up the database and tearing it down
@pytest.fixture(scope="module")
def setup_database():
    # Setup: Create the tables
    create_tables()
    yield
    # Teardown: Drop the tables after the tests
    drop_all_tables()


# Test the create_team function
def test_create_team(setup_database):
    team_name = "Dream Team1"
    player_ids = [1, 2, 3, 7, 12]

    team_id = create_team(team_name, player_ids)

    assert team_id is not None
    assert team_id > 0


# Test the update_team function
def test_update_team(setup_database):
    # Create an initial team
    team_name = "Initial Team"
    initial_player_ids = [4, 5]
    team_id = create_team(team_name, initial_player_ids)

    # Update the team with new players
    new_player_ids = [6, 7, 8]
    updated_team_id = update_team(team_id, new_player_ids)

    assert updated_team_id == team_id  # Ensure the same team was updated


# Test the delete_team function
def test_delete_team(setup_database):
    # Create a team to be deleted
    team_name = "Temporary Team"
    player_ids = [9, 10]
    team_id = create_team(team_name, player_ids)

    # Delete the team
    is_deleted = delete_team(team_id)

    assert is_deleted is True  # Ensure the team was deleted successfully


# Test the get_team_name_by_id function
def test_get_team_name_by_id(setup_database):
    # Create a team to retrieve
    team_name = "Retrievable Team"
    player_ids = [11, 12]
    team_id = create_team(team_name, player_ids)

    # Retrieve the team name by ID
    retrieved_team_name = get_team_name_by_id(team_id)

    assert retrieved_team_name == team_name  # Ensure the correct name is retrieved