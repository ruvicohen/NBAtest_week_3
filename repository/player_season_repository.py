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

def extract_season_player_from_nba_data(nba_data, player_id):
    return PlayerSeasonStatus(
        player_id=player_id,
        team=nba_data["team"],
        position=nba_data["position"],
        seasons=nba_data["season"],
        points=nba_data["points"],
        games=nba_data["games"],
        assists=nba_data["assists"],
        turnovers=nba_data["turnovers"],
        two_percent=nba_data["twoPercent"],
        three_percent=nba_data["threePercent"]

    )

def get_player_season():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            SELECT * FROM player_season
        ''')
        result = cursor.fetchall()
        return result

def get_players_by_position_and_season(position, season):
    if not season:
        query = "SELECT * FROM player_season WHERE position = %s"
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