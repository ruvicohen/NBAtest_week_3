from dataclasses import dataclass, field
from typing import List

from models.player_season_status import PlayerSeasonStatus


@dataclass
class FantasyTeam:
    team: str
    players: List[PlayerSeasonStatus]