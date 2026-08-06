from dataclasses import dataclass


@dataclass
class LiveInfo:

    # ---------------------------------------
    # Overview
    # ---------------------------------------

    live_gpm: str = ""

    live_gpm_value: float = 0

    live_streams: str = ""

    live_streams_value: int = 0

    average_live_views: str = ""

    average_live_views_value: int = 0

    average_live_engagement_rate: str = ""

    average_live_engagement_rate_value: float = 0

    # ---------------------------------------
    # Carousel Metrics
    # ---------------------------------------

    average_live_likes: str = ""

    average_live_likes_value: int = 0

    average_live_comments: str = ""

    average_live_comments_value: int = 0

    average_live_shares: str = ""

    average_live_shares_value: int = 0