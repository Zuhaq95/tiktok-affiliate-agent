from dataclasses import dataclass


@dataclass
class FollowersInfo:

    female_percentage: float | None = None

    male_percentage: float | None = None

    top_country: str = ""

    top_age_group: str = ""