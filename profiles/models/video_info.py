from dataclasses import dataclass


@dataclass
class VideoInfo:

    video_gpm: str = ""

    video_gpm_value: float = 0

    videos: int = 0

    average_video_views: str = ""

    average_video_views_value: int = 0

    average_video_engagement_rate: str = ""

    average_video_engagement_rate_value: float = 0