def get_atr(assists, turnovers ):
    return assists / turnovers if turnovers > 0 else 0


def get_ppg_ratio(points_per_game, average_per_position):
    return points_per_game / average_per_position


def get_points_per_game(points, games):
    return points / games if games > 0 else 0


