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

    def __str__(self):
        return (
            f"""
====================================================
Creator
----------------------------------------------------
Username      : {self.username}
Name          : {self.name}
Followers     : {self.followers}
Category      : {self.category}

GMV           : {self.gmv}
Items Sold    : {self.items_sold}
Avg Views     : {self.avg_views}
Engagement    : {self.engagement}
====================================================
"""
        )