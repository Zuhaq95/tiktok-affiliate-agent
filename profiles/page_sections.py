from dataclasses import dataclass

from playwright.sync_api import Locator


@dataclass
class PageSections:
    """
    Holds the locator for every major section of the
    Creator Details page.
    """

    # Creator header
    header: Locator

    # Navigation tabs
    navigation: Locator

    # Sales
    sales: Locator

    # Sales charts
    sales_charts: Locator

    # Collaboration
    collaboration: Locator

    # Video
    video: Locator

    # LIVE
    live: Locator

    # Followers
    followers: Locator

    # Trends
    trends: Locator

    # Example Videos
    example_videos: Locator

    # Product Videos
    product_videos: Locator