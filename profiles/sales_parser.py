from playwright.sync_api import Page

from profiles.models.sales_info import SalesInfo

from profiles.helpers.metric_card_parser import MetricCardParser
from profiles.helpers.carousel_navigator import CarouselNavigator
from profiles.helpers.distribution_parser import DistributionParser


class SalesParser:
    """
    Parses the complete Sales section.

    Extracts

    - Overview metrics
    - GMV by sales channel
    - GMV by product category
    """

    def __init__(self, page: Page):

        self.page = page

    # ---------------------------------------------------------

    def parse(self, sales: SalesInfo):

        print("Parsing sales...")

        self.wait_until_loaded()

        section = self.sales_section()

        metric_parser = MetricCardParser(section)
        navigator = CarouselNavigator(section)

        metrics = {}

        # First page
        metrics.update(
            metric_parser.parse_visible()
        )

        # Remaining carousel pages
        while navigator.move_next():

            metrics.update(
                metric_parser.parse_visible()
            )

        # -------------------------
        # Overview
        # -------------------------

        sales.total_gmv = metrics.get(
            "GMV",
            ""
        )

        sales.items_sold = metrics.get(
            "Items sold",
            ""
        )

        sales.gpm = metrics.get(
            "GPM",
            ""
        )

        sales.gmv_per_customer = metrics.get(
            "GMV per customer",
            ""
        )

        # -------------------------
        # Distributions
        # -------------------------

        parser = DistributionParser(section)

        sales.sales_channel_distribution = (
            parser.parse(
                "GMV per sales channel"
            )
        )

        sales.category_distribution = (
            parser.parse(
                "GMV by product category"
            )
        )

        print("✓ Sales parsed")

    # ---------------------------------------------------------

    def wait_until_loaded(self):

        self.page.locator(
            "text=GMV per customer"
        ).wait_for(timeout=10000)

    # ---------------------------------------------------------

    def sales_section(self):

        return (
            self.page.locator("text=Sales")
            .locator("..")
            .locator("..")
        )