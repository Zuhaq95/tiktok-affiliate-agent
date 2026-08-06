import re

from playwright.sync_api import Locator

from profiles.models.collaboration_info import CollaborationInfo

from profiles.helpers.metric_card_parser import MetricCardParser
from profiles.helpers.carousel_navigator import CarouselNavigator
from profiles.helpers.parser_utils import ParserUtils


class CollaborationParser:
    """
    Parses the Collaboration section.

    Responsibility:
        - Parse collaboration metrics
        - Parse product price range

    It never searches the page.
    It only parses the section it is given.
    """

    # ---------------------------------------------------------

    def parse(
        self,
        section: Locator,
        collaboration: CollaborationInfo
    ):

        print("Parsing collaboration...")

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
        # Estimated Post Rate
        # ---------------------------------------

        collaboration.estimated_post_rate = metrics.get(
            "Est. post rate",
            ""
        )

        if collaboration.estimated_post_rate:

            collaboration.estimated_post_rate_value = (
                ParserUtils.percent_to_float(
                    collaboration.estimated_post_rate
                )
            )

        # ---------------------------------------
        # Average Commission Rate
        # ---------------------------------------

        collaboration.average_commission_rate = metrics.get(
            "Avg. commission rate",
            ""
        )

        if collaboration.average_commission_rate:

            collaboration.average_commission_rate_value = (
                ParserUtils.percent_to_float(
                    collaboration.average_commission_rate
                )
            )

        # ---------------------------------------
        # Products
        # ---------------------------------------

        collaboration.products = metrics.get(
            "Products",
            ""
        )

        if collaboration.products:

            collaboration.products_value = (
                ParserUtils.count_to_int(
                    collaboration.products
                )
            )

        # ---------------------------------------
        # Brand Collaborations
        # ---------------------------------------

        collaboration.brand_collaborations = metrics.get(
            "Brand collaborations",
            ""
        )

        if collaboration.brand_collaborations:

            collaboration.brand_collaborations_value = (
                ParserUtils.count_to_int(
                    collaboration.brand_collaborations
                )
            )

        # ---------------------------------------
        # Product Price
        # ---------------------------------------

        collaboration.product_price = metrics.get(
            "Product price",
            ""
        )

        self.parse_price_range(collaboration)

        print("✓ Collaboration parsed")

    # ---------------------------------------------------------

    def parse_price_range(
        self,
        collaboration: CollaborationInfo
    ):

        if not collaboration.product_price:
            return

        values = re.findall(
            r"[\d.]+",
            collaboration.product_price
        )

        if len(values) >= 2:

            collaboration.minimum_product_price = float(
                values[0]
            )

            collaboration.maximum_product_price = float(
                values[1]
            )