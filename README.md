# NBA Fantasy App

This Flask application allows users to create and manage NBA fantasy teams, search for players, and compare team statistics.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/benitalker/nba-fantasy-app
   cd nba-fantasy-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install flask toolz pytest requests psycopg2-binary
   ```

4. Set up the database:
   - Create a PostgreSQL database named `nba_db`
   - Update the `SQLALCHEMY_DATABASE_URI` in `config.py` with your database credentials

5. Collect initial data:
   ```
   make sure to run the seed()
   ```

6. Run the application:
   ```
   python run.py
   ```

The application should now be running on your localhost.

## Running Tests

To run the tests, use the following command:
```
pytest
```

## API Endpoints

- GET `/api/players?position={position}&season={season}`: Get players by position and season
- POST `/api/teams`: Create a new fantasy team
- GET `/api/teams/<team_id>`: Get details of a specific team
- PUT `/api/teams/<team_id>`: Update a team's players
- DELETE `/api/teams/<team_id>`: Delete a team
- GET `/api/teams/compare?team={team_id}&team={team_id}...`: Compare multiple fantasy teams
- GET '/api/teams/stats?team1={team_name1}&team2={team_name2}&...': compare teams by name: BOS, TOR......

