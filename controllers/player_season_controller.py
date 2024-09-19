from flask import Blueprint, jsonify, request
from repository.database import get_players_by_position_and_season

player_blueprint = Blueprint("player", __name__)


@player_blueprint.route("/players", methods=["GET"])
def get_players():
    position = request.args.get('position')
    season = request.args.get('season', None)

    if not position:
        return jsonify({"error": "Position is required"}), 400

    try:
        season = int(season) if season else None
    except ValueError:
        return jsonify({"error": "Season must be an integer"}), 400

    players = get_players_by_position_and_season(position, season)

    return jsonify({"players": players}), 200
