from dataclasses import dataclass


@dataclass
class TrendInfo:

    gmv_trend: list[float] | None = None

    units_sold_trend: list[float] | None = None

    followers_trend: list[float] | None = None

    video_views_trend: list[float] | None = None

    engagement_trend: list[float] | None = None