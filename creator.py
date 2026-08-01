from dataclasses import dataclass, field


@dataclass
class Creator:
    # Basic Information
    name: str = ""
    username: str = ""

    # Raw TikTok Values
    followers: str = ""
    gender_age: str = ""

    category: str = ""

    gmv: str = ""
    items_sold: str = ""
    avg_views: str = ""
    engagement: str = ""

    previously_invited: bool = False

    # Normalized Values
    followers_value: int = 0
    gmv_value: float = 0.0
    items_sold_value: float = 0.0
    avg_views_value: float = 0.0
    engagement_value: float = 0.0

    # AI Results
    ai_score: float = 0.0
    ai_reasons: list[str] = field(default_factory=list)

    def __str__(self):
        return (
            f"""
====================================================
Creator
----------------------------------------------------
Username          : {self.username}
Name              : {self.name}

Followers         : {self.followers}
Category          : {self.category}

GMV               : {self.gmv}
Items Sold        : {self.items_sold}
Avg Views         : {self.avg_views}
Engagement        : {self.engagement}

AI Score          : {self.ai_score:.2f}
====================================================
"""
        )