from dataclasses import dataclass


@dataclass
class VideoInfo:

    average_views: str = ""

    average_likes: str = ""

    average_comments: str = ""

    average_shares: str = ""

    engagement_rate: float | None = None