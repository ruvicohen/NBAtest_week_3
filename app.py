from flask import Flask

from controllers.fantasy_team_controller import teams_blueprint
from controllers.player_season_controller import player_blueprint
from repository.database import drop_all_tables
from services.seed import seed

app = Flask(__name__)

if __name__ == "__main__":
    seed()
    app.register_blueprint(teams_blueprint, url_prefix="/api/teams")
    app.register_blueprint(player_blueprint, url_prefix="/api/players")
    app.run(debug=True)