from dataclasses import dataclass


@dataclass
class TrendInfo:

    gmv_trend: list[float | None] | None = None

    units_sold_trend: list[float | None] | None = None

    followers_trend: list[float | None] | None = None

    video_views_trend: list[float | None] | None = None

    engagement_trend: list[float | None] | None = None

    