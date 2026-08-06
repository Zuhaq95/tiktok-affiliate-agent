from dataclasses import dataclass


@dataclass
class VideoInfo:

    # ---------------------------------------
    # Overview
    # ---------------------------------------

    video_gpm: str = ""

    video_gpm_value: float = 0

    videos: str = ""

    videos_value: int = 0

    average_video_views: str = ""

    average_video_views_value: int = 0

    average_video_engagement_rate: str = ""

    average_video_engagement_rate_value: float = 0

    # ---------------------------------------
    # Carousel Metrics
    # ---------------------------------------

    average_video_likes: str = ""

    average_video_likes_value: int = 0

    average_video_comments: str = ""

    average_video_comments_value: int = 0

    average_video_shares: str = ""

    average_video_shares_value: int = 0