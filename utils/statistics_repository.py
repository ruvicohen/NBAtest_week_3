def calculate_team_statistics(players):
    points = sum(map(lambda x: x["points"], players))
    twoPercent = sum(map(lambda x: x["twopercent"] if x["twopercent"] else 0, players))
    threePercent = sum(map(lambda x: x["threepercent"] if x["threepercent"] else 0, players))
    atr = sum(map(lambda x: x["atr"], players))
    PPG_Ratio = sum(map(lambda x: x["ppg_ratio"], players))

    return {"points": points, "two_percent": twoPercent, "three_percent": threePercent, "atr": atr,
            "ppg_ratio": PPG_Ratio}
