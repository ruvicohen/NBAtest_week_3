from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(teams_blueprint, url_prefix="/api/teams")
    app.register_blueprint(player_blueprint, url_prefix="/api/players")
    app.run(debug=True)