from toolz import curry, pipe, juxt
from toolz.curried import partial


def get_atr(assists, turnovers):
    return assists / turnovers if turnovers > 0 else 0

def get_ppg_ratio(player, nba_data):
    return get_points_per_game(player) / get_average_ppg_per_position(nba_data, player["position"])

def get_points_per_game(player):
    return player["points"] / player["games"] if player["games"] > 0 else 0

@curry
def get_average_ppg_per_position1(nba_data, position):
    return pipe(
        nba_data,
        partial(filter, lambda player: player['position'] == position),
        partial(juxt,[partial(map, lambda player: player['games']),partial(map, lambda player: player['points'] ) ]),
        lambda sum_games: sum(sum_games[0]) / sum(sum_games[1])

    )
def get_average_ppg_per_position(nba_data, position):
    # Filter players by position
    list_filter = list(filter(lambda player: player['position'] == position, nba_data))

    # Calculate the sum of games and points for the filtered players
    sum_games = sum(map(lambda player: player['games'], list_filter))
    sum_points = sum(map(lambda player: player['points'], list_filter))

    # Ensure there are games to avoid division by zero
    return sum_points / sum_games if sum_games > 0 else 0

# @curry
# def get_average_ppg_per_position(nba_data, position):
#     filtered_data = filter(lambda player: player['position'] == position, nba_data)
#
#     # Calculate sum of games and sum of points for the position
#     games_points = juxt(
#         lambda players: sum(map(lambda player: player['games'], players)),
#         lambda players: sum(map(lambda player: player['points'], players))
#     )
#
#     total_games, total_points = games_points(filtered_data)
#
#     return total_points / total_games if total_games > 0 else 0