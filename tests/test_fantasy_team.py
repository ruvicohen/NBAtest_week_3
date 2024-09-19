import pytest
from repository.database import create_tables, drop_all_tables
from repository.fantasy_team_repository import create_team, update_team, delete_team, get_team_name_by_id

@pytest.fixture(scope="module")
def setup_database():
    create_tables()
    yield
    drop_all_tables()


@pytest.fixture
def player_ids():
    return [1, 2, 3]


@pytest.fixture
def team_name():
    return "Dream Team"


# Test the create_team function
def test_create_team(setup_database, team_name, player_ids):
    team_id = create_team(team_name, player_ids)
    assert team_id is not None
    retrieved_team_name = get_team_name_by_id(team_id)
    assert retrieved_team_name == team_name


# Test the update_team function
def test_update_team(setup_database, team_name, player_ids):
    team_id = create_team(team_name, player_ids)
    new_player_ids = [4, 5, 6]
    updated_team_id = update_team(team_id, new_player_ids)

    # Ensure the team ID remains the same
    assert updated_team_id == team_id



# Test the delete_team function
def test_delete_team(setup_database, team_name, player_ids):
    # First, create a team
    team_id = create_team(team_name, player_ids)

    # Delete the team and verify deletion
    deleted = delete_team(team_id)
    assert deleted is True

    # Ensure the team no longer exists
    deleted_team_name = get_team_name_by_id(team_id)
    assert deleted_team_name is None


# Test the get_team_name_by_id function
def test_get_team_name_by_id(setup_database, team_name, player_ids):
    # Create a team
    team_id = create_team(team_name, player_ids)

    # Retrieve the team name by its ID
    retrieved_team_name = get_team_name_by_id(team_id)

    # Ensure the retrieved name matches the original team name
    assert retrieved_team_name == team_name

    # Try to retrieve a non-existent team
    non_existent_team = get_team_name_by_id(99999)
    assert non_existent_team is None
