from dataclasses import dataclass, field


@dataclass
class CreatorProfile:
    """
    Stores detailed information extracted from the
    Creator Details page.

    This object is attached to a Creator after
    deep profile analysis.

    Creator
        └── profile
    """

    # -----------------------------
    # Sales Overview
    # -----------------------------

    gmv: str = ""
    items_sold: str = ""
    gpm: str = ""
    gmv_per_customer: str = ""

    # -----------------------------
    # GMV by Product Category
    # -----------------------------

    category_distribution: dict = field(default_factory=dict)

    # Example:
    # {
    #     "Textiles & Soft Furnishings": 98.4,
    #     "Home Supplies": 1.6
    # }

    # -----------------------------
    # Sales Channels
    # -----------------------------

    video_sales_percentage: float = 0
    live_sales_percentage: float = 0

    # -----------------------------
    # Top Products
    # -----------------------------

    top_products: list = field(default_factory=list)

    # -----------------------------
    # Top Videos
    # -----------------------------

    top_videos: list = field(default_factory=list)

    # -----------------------------
    # Audience
    # -----------------------------

    audience_gender: dict = field(default_factory=dict)

    audience_age: dict = field(default_factory=dict)

    audience_location: dict = field(default_factory=dict)

    # -----------------------------
    # Trend
    # -----------------------------

    trend: str = ""

    # -----------------------------
    # Deep AI
    # -----------------------------

    deep_score: float = 0

    confidence: float = 0

    evidence: list[str] = field(default_factory=list)