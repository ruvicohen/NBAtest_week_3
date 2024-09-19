import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URI

def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)

def create_player_season_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_season (
            id SERIAL PRIMARY KEY,
            player_id INT NOT NULL,
            team VARCHAR(255) NOT NULL,
            position VARCHAR(255) NOT NULL,
            seasons INT NOT NULL,
            points INT NOT NULL,
            games INT NOT NULL,
            assists INT NOT NULL,
            turnovers INT NOT NULL,
            two_percent FLOAT,
            three_percent FLOAT,
            atr FLOAT NOT NULL,  
            ppg_ratio FLOAT NOT NULL,  
            FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE
        )
        ''')
        connection.commit()

def create_fantasy_team_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS fantasy_team (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        ''')
        connection.commit()

def create_player_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        ''')
        connection.commit()

def create_player_fantasy_team_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_fantasy_team (
            id SERIAL PRIMARY KEY,
            player_id INT NOT NULL,
            fantasy_team_id INT NOT NULL,
            FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE,
            FOREIGN KEY (fantasy_team_id) REFERENCES fantasy_team(id) ON DELETE CASCADE
        )
        ''')
        connection.commit()

def create_tables():
    create_player_table()
    create_fantasy_team_table()
    create_player_season_table()
    create_player_fantasy_team_table()

def drop_all_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS player_fantasy_team;
        DROP TABLE IF EXISTS player_season;
        DROP TABLE IF EXISTS fantasy_team;
        DROP TABLE IF EXISTS player;
    ''')

    connection.commit()
    cursor.close()
    connection.close()


