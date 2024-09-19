
from models.player_season_status import PlayerSeasonStatus
from repository.database import get_db_connection


def create_player_season(player_season: PlayerSeasonStatus):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO player_season (
                player_id, team, position, seasons, points, games,assists,turnovers, two_percent, three_percent, atr, ppg_ratio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            player_season.player_id,
            player_season.team,
            player_season.position,
            player_season.seasons,
            player_season.points,
            player_season.games,
            player_season.assists,
            player_season.turnovers,
            player_season.two_percent,
            player_season.three_percent,
            player_season.atr,
            player_season.ppg_ratio
        ))
        connection.commit()
        new_id = cursor.fetchone()['id']
        return new_id


def get_player_season():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM player_season
        ''')
        result = cursor.fetchall()
        return result

def get_players_by_position_and_season(position, season):
    if not season:
        query = """
                SELECT 
                p.name AS player_name,          
                ps.player_id,
                ps.position,
                SUM(ps.points) AS total_points,
                SUM(ps.assists) AS total_assists,
                SUM(ps.turnovers) AS total_turnovers,
                SUM(ps.games) AS total_games,
                AVG(ps.two_percent) AS avg_two_percent,
                AVG(ps.three_percent) AS avg_three_percent,
                SUM(ps.points) / SUM(ps.games) AS points_per_game  
                FROM player_season ps
                JOIN player p ON ps.player_id = p.id  
                WHERE ps.position = %s                 
                GROUP BY ps.player_id, ps.position, p.name 

        """
        params = (position,)
    else:
        query = "SELECT * FROM player_season WHERE position = %s AND seasons = %s"
        params = (position, season)

    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result


def get_by_season(season: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM player_season WHERE seasons = %s
        ''', (season,))
        result = cursor.fetchall()
        return result


# Function to get player seasons by player_id
def get_by_player_id(player_id: int):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM player_season WHERE player_id = %s
        ''', (player_id,))
        result = cursor.fetchall()
        return result

def get_players_by_ids(player_ids):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.executemany('INSERT INTO player_fantasy_team (player_id) VALUES (%s)',
                           [player_id for player_id in player_ids])

        connection.commit()
        players = cursor.fetchall()
    return players




def get_players_by_team_id(team_id):
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
                SELECT 
                p.name AS player_name,          
                ps.player_id,
                ps.position,
                SUM(ps.points) AS total_points,
                SUM(ps.assists) AS total_assists,
                SUM(ps.turnovers) AS total_turnovers,
                SUM(ps.games) AS total_games,
                AVG(ps.two_percent) AS avg_two_percent,
                AVG(ps.three_percent) AS avg_three_percent,
                SUM(ps.points) / SUM(ps.games) AS points_per_game
                FROM player p
                JOIN player_fantasy_team pft ON p.id = pft.player_id
                JOIN player_season ps ON p.id = ps.player_id
                WHERE pft.fantasy_team_id = %s
                GROUP BY ps.player_id, ps.position, p.name 
        ''', (team_id,))

        players = cursor.fetchall()
        return players
