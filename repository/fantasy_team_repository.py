from repository.database import get_db_connection

def create_team(team_name, player_ids):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('INSERT INTO fantasy_team (name) VALUES (%s) RETURNING id', (team_name,))
        team_id = cursor.fetchone()[0]
        connection.commit()

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.executemany('INSERT INTO player_fantasy_team (player_id, fantasy_team_id) VALUES (%s, %s)',
                           [(player_id, team_id) for player_id in player_ids])
        connection.commit()

    return team_id




