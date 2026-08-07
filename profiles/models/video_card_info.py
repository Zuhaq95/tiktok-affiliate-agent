from dataclasses import dataclass


@dataclass
class VideoCardInfo:
    """
    Represents a single video card shown in the
    Creator Details page.
    """

    # ---------------------------------------
    # Thumbnail
    # ---------------------------------------

    thumbnail_url: str = ""

    # ---------------------------------------
    # Content
    # ---------------------------------------

    caption: str = ""

    release_time: str = ""

    # ---------------------------------------
    # Metrics
    # ---------------------------------------

    views: str = ""

    views_value: int = 0

    likes: str = ""

    likes_value: int = 0

    # ---------------------------------------
    # Links
    # ---------------------------------------

    tiktok_url: str = ""

    has_products: bool = False