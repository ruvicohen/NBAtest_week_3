from dataclasses import asdict

from flask import Blueprint, jsonify, request

from dto.ResponseDto import ResponseDto
from repository.player_season_repository import get_players_by_position_and_season, get_player_season

player_blueprint = Blueprint("player", __name__)

@player_blueprint.route("/", methods=["GET"])
def get_players():
    position = request.args.get('position')
    season = request.args.get('season', None)

    if not position:
        response = ResponseDto(error="Position is required")
        return jsonify(asdict(response)), 400

    try:
        season = int(season) if season else None
    except ValueError:
        response = ResponseDto(error="Season must be an integer")
        return jsonify(asdict(response)), 400

    players = get_players_by_position_and_season(position, season)
    response = ResponseDto(body={"players": players})
    return jsonify(asdict(response)), 200