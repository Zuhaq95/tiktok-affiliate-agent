from dataclasses import dataclass, field


@dataclass
class SalesInfo:

    # -----------------------------
    # Overview
    # -----------------------------

    total_gmv: str = ""
    total_gmv_value: float = 0

    items_sold: str = ""
    items_sold_value: int = 0

    gpm: str = ""
    gpm_value: float = 0

    gmv_per_customer: str = ""
    gmv_per_customer_value: float = 0

    # -----------------------------
    # Sales Channels
    # -----------------------------

    video_percentage: float = 0

    live_percentage: float = 0

    # -----------------------------
    # Category Distribution
    # -----------------------------

    category_distribution: dict[str, float] = field(
        default_factory=dict
    )

    # -----------------------------
    # Trend
    # -----------------------------

    monthly_gmv: list[float] = field(
        default_factory=list
    )

    monthly_units: list[int] = field(
        default_factory=list
    )