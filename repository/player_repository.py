from models.player import Player
from repository.database import get_db_connection


def create_player(player: Player) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO player (name) VALUES (%s) RETURNING id",
            (player.name, )
        )
        new_id = cursor.fetchone()["id"]
        connection.commit()
        return new_id

def extract_player_from_nba_data(nba_data) -> Player:
    return Player(
        name=nba_data["playerName"]
    )

def get_player_id_by_name(player_name: str) -> int:
    with get_db_connection() as connection, connection.cursor() as cursor:
        query = """
        SELECT id 
        FROM player 
        WHERE name = %s
        """
        cursor.execute(query, (player_name,))
        result = cursor.fetchone()

        return result['id'] if result else None


