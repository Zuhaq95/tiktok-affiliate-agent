from dataclasses import dataclass, field


@dataclass
class SalesInfo:

    # -----------------------------
    # Report Period
    # -----------------------------

    report_period: str = ""

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
    # Sales Channel Distribution
    # -----------------------------

    sales_channel_distribution: dict[str, float] = field(
        default_factory=dict
    )

    # -----------------------------
    # Product Category Distribution
    # -----------------------------

    category_distribution: dict[str, float] = field(
        default_factory=dict
    )