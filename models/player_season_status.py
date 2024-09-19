from dataclasses import dataclass, field
from typing import List

@dataclass
class PlayerSeasonStatus:
    player_id: int
    team: str
    position: str
    seasons: int
    points: int
    games: int
    assists: int
    turnovers: int
    two_percent: float
    three_percent: float
    atr: float = None  # Assist-to-Turnover Ratio
    ppg_ratio: float = None  # Points Per Game Ratio (compared to position average)
    id: int = None

