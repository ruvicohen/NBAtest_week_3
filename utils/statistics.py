from toolz import pipe, juxt
from toolz.curried import partial


def calculate_team_statistics(players):
    points = sum(map(lambda x: x["total_points"], players))
    twoPercent = sum(map(lambda x: x["avg_two_percent"] if x["avg_two_percent"] else 0, players))
    threePercent = sum(map(lambda x: x["avg_three_percent"] if x["avg_three_percent"] else 0, players))
    atr = sum(map(lambda x: x["avg_atr"] if x["avg_atr"] else 0, players))
    ppg_ratio = sum(map(lambda x: x["avg_ppg_ratio"] if x["avg_ppg_ratio"] else 0, players))

    return {"team_name": players[0]["team_name"] ,"points": points, "two_percent": twoPercent, "three_percent": threePercent, "atr": atr,
            "ppg_ratio": ppg_ratio}

def calculate_team_statistics1(players):
    return pipe(
        partial(juxt,
            partial(map, lambda x: x["total_points"]),
            partial(map, lambda x: x["avg_two_percent"] if x["avg_two_percent"] else 0),
            partial(map, lambda x: x["avg_three_percent"] if x["avg_three_percent"] else 0),
            partial(map, lambda x: x["avg_atr"]),
            partial(map, lambda x: x["avg_ppg_ratio"])
        ),
        partial(map, sum),
        lambda team_statistics: {"team_name": players[0]["team_name"] ,
                                 "points": team_statistics[0],
                                 "two_percent": team_statistics[1],
                                 "three_percent": team_statistics[2],
                                 "atr": team_statistics[3],
                                 "ppg_ratio": team_statistics[4]}
    )