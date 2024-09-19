from flask import Blueprint, request, jsonify
from dto.ResponseDto import ResponseDto
from repository.fantasy_team_repository import create_team, update_team, delete_team, get_team_name_by_id
from repository.player_season_repository import get_by_player_id, get_players_by_team_id
from utils.statistics_repository import calculate_team_statistics


teams_blueprint = Blueprint("teams", __name__)

@teams_blueprint.route("/", methods=["POST"])
def create_fantasy_team():
    data = request.get_json()
    team_name = data.get("team_name")
    player_ids = data.get("player_ids")

    if len(player_ids) < 5:
        return jsonify(ResponseDto(error="At least 5 players are required")), 400

    positions = set()
    for player_id in player_ids:
        player = get_by_player_id(player_id)
        if player:
            positions.add(player[0]["position"])
        else:
            return jsonify(ResponseDto(error=f"Player with ID {player_id} not found")), 404

    if len(positions) < 5:
        return jsonify(ResponseDto(error="A player is required for each position")), 400

    team_id = create_team(team_name, player_ids)
    return jsonify(ResponseDto(message="Team created successfully", body={"team_id": team_id, "team_name": team_name})), 201

@teams_blueprint.route("/<int:team_id>", methods=["PUT"])
def update_team_endpoint(team_id):
    data = request.get_json()
    player_ids = data.get("player_ids")

    if len(player_ids) < 5:
        return jsonify(ResponseDto(error="At least 5 players are required")), 400

    positions = set()
    for player_id in player_ids:
        player = get_by_player_id(player_id)
        if player:
            if isinstance(player, list):
                positions.add(player[0]["position"])
            else:
                positions.add(player["position"])
        else:
            return jsonify(ResponseDto(error=f"Player with ID {player_id} not found")), 404

    if len(positions) < 5:
        return jsonify(ResponseDto(error="A player is required for each position")), 400

    updated_team_id = update_team(team_id, player_ids)
    return jsonify(ResponseDto(message="Team updated successfully", body={"team_id": updated_team_id})), 200

@teams_blueprint.route("/<int:team_id>", methods=["DELETE"])
def delete_fantasy_team(team_id):
    success = delete_team(team_id)

    if success:
        return jsonify(ResponseDto(message=f"Team with id {team_id} has been deleted successfully")), 200
    else:
        return jsonify(ResponseDto(error=f"Team with id {team_id} not found")), 404

@teams_blueprint.route("/<int:team_id>", methods=["GET"])
def get_team_details(team_id):
    team = get_team_name_by_id(team_id)
    if not team:
        return jsonify(ResponseDto(error="Team not found")), 404

    players = get_players_by_team_id(team_id)
    return jsonify(ResponseDto(message="Team found", body={"team_name": team, "players": players})), 200

@teams_blueprint.route("/compare", methods=["GET"])
def compare_teams_endpoint():
    query_params = request.args
    team_ids = [int(query_params[key]) for key in query_params if key.startswith('team')]

    if len(team_ids) < 2:
        return jsonify(ResponseDto(error="At least 2 teams are required for comparison")), 400

    teams = []
    for team_id in team_ids:
        team = get_team_name_by_id(int(team_id))
        if not team:
            return jsonify(ResponseDto(error=f"Team with ID {team_id} not found")), 404
        teams.append(team)

    team_stats = []
    for team in team_ids:
        players = get_players_by_team_id(team)
        average_stats = calculate_team_statistics(players)
        team_stats.append({
            "team": team,
            "points": average_stats["points"],
            "twoPercent": average_stats["two_percent"],
            "threePercent": average_stats["three_percent"],
            "ATR": average_stats["atr"],
            "PPG Ratio": average_stats["ppg_ratio"]
        })

    sorted_teams = sorted(team_stats, key=lambda x: x["PPG Ratio"], reverse=True)
    return jsonify(ResponseDto(message="Teams compared successfully", body=sorted_teams)), 200
