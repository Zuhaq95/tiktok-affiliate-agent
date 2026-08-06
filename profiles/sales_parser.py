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
    It only parses the sections it is given.
    """

    # ---------------------------------------------------------

    def parse(
        self,
        metrics_section: Locator,
        charts_section: Locator,
        sales: SalesInfo
    ):

        print("Parsing sales...")

        metric_parser = MetricCardParser(
            metrics_section
        )

        navigator = CarouselNavigator(
            metrics_section
        )

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

        print(f"✓ Parsed {len(metrics)} overview metrics")

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
            charts_section
        )

        sales.sales_channel_distribution = (
            distribution_parser.parse(
                "GMV per sales channel"
            )
        )

        print(
            f"✓ Parsed {len(sales.sales_channel_distribution)} sales channel entries"
        )

        sales.category_distribution = (
            distribution_parser.parse(
                "GMV by product category"
            )
        )

        print(
            f"✓ Parsed {len(sales.category_distribution)} product category entries"
        )

        print("✓ Sales parsed")