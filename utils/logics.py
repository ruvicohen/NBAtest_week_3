def get_atr(assists, turnovers ):
    return assists / turnovers if turnovers > 0 else 0


def get_ppg_ratio(points_per_game, average_per_position):
    return points_per_game / average_per_position


def get_points_per_game(points, games):
    return points / games if games > 0 else 0

def get_average_ppg_position(nba_data, position):
    filter_list = list(filter(lambda player: player['position'] == position, nba_data))
    sum_games = sum(list(map(lambda player: player['games'], filter_list)))
    sum_points = sum(list(map(lambda player: player['points'], filter_list)))
    return sum_points / sum_games