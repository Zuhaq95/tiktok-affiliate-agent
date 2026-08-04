from dataclasses import dataclass, field


@dataclass
class FollowersInfo:

    male_percentage: float = 0

    female_percentage: float = 0

    top_locations: list[str] = field(default_factory=list)

    age_groups: dict[str, float] = field(default_factory=dict)