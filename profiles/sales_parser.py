from playwright.sync_api import Locator

from profiles.models.sales_info import SalesInfo

from profiles.helpers.metric_card_parser import MetricCardParser
from profiles.helpers.carousel_navigator import CarouselNavigator
from profiles.helpers.distribution_parser import DistributionParser


class SalesParser:
    """
    Parses the complete Sales section.

    Responsibility:
        - Parse overview metrics
        - Parse sales distributions

    It never searches the page.
    It only parses the section it is given.
    """

    # ---------------------------------------------------------

    def parse(
        self,
        section: Locator,
        sales: SalesInfo
    ):

        print("Parsing sales...")

        metric_parser = MetricCardParser(section)
        navigator = CarouselNavigator(section)

        metrics = {}

        # ---------------------------------------
        # Metric Cards
        # ---------------------------------------

        metrics.update(
            metric_parser.parse_visible()
        )

        while navigator.move_next():

            metrics.update(
                metric_parser.parse_visible()
            )

        # ---------------------------------------
        # Overview
        # ---------------------------------------

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

        # ---------------------------------------
        # Distribution Charts
        # ---------------------------------------

        distribution_parser = DistributionParser(
            section
        )

        sales.sales_channel_distribution = (
            distribution_parser.parse(
                "GMV per sales channel"
            )
        )

        sales.category_distribution = (
            distribution_parser.parse(
                "GMV by product category"
            )
        )

        print("✓ Sales parsed")