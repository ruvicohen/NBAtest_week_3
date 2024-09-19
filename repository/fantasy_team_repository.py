from repository.database import get_db_connection

def create_team(team_name, player_ids):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('INSERT INTO fantasy_team (name) VALUES (%s) RETURNING id', (team_name,))
        team_id = cursor.fetchone()["id"]
        connection.commit()

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.executemany('INSERT INTO player_fantasy_team (player_id, fantasy_team_id) VALUES (%s, %s)',
                           [(player_id, team_id) for player_id in player_ids])
        connection.commit()

    return team_id


def update_team(team_id, player_ids):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM player_fantasy_team WHERE fantasy_team_id = %s', (team_id,))

        cursor.executemany('INSERT INTO player_fantasy_team (player_id, fantasy_team_id) VALUES (%s, %s)',
                           [(player_id, team_id) for player_id in player_ids])

        connection.commit()

    return team_id


def delete_team(team_id):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM player_fantasy_team WHERE fantasy_team_id = %s', (team_id,))
        cursor.execute('DELETE FROM fantasy_team WHERE id = %s', (team_id,))

        deleted_rows = cursor.rowcount
        connection.commit()

    return deleted_rows > 0


