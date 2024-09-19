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

def delete_player(player_id):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM player WHERE id = %s', (player_id,))
        deleted_rows = cursor.rowcount
        connection.commit()

    return deleted_rows > 0


