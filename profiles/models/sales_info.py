from dataclasses import dataclass


@dataclass
class SalesInfo:

    total_gmv: str = ""

    items_sold: str = ""

    gpm: str = ""

    gmv_per_customer: str = ""

    video_percentage: float | None = None

    live_percentage: float | None = None