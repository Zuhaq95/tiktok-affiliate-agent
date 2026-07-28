from dataclasses import dataclass


@dataclass
class Creator:

    name: str = ""
    username: str = ""

    followers: str = ""
    gender_age: str = ""

    category: str = ""

    gmv: str = ""
    items_sold: str = ""
    avg_views: str = ""
    engagement: str = ""

    previously_invited: bool = False