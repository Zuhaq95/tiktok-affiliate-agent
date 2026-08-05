from playwright.sync_api import Page

from profiles.models.sales_info import SalesInfo

from profiles.helpers.metric_card_parser import MetricCardParser
from profiles.helpers.parser_utils import ParserUtils


class SalesParser:
    """
    Parses the Sales section.

    Extracts:

        - GMV
        - Items Sold
        - GPM
        - GMV per customer
    """

    def __init__(self, page: Page):

        self.page = page

    # ---------------------------------------------------------

    def parse(self, sales: SalesInfo):

        print("Parsing sales...")

        self.wait_until_loaded()

        cards = MetricCardParser(
            self.page
        ).parse()

        # -------------------------------------
        # GMV
        # -------------------------------------

        sales.total_gmv = cards.get("GMV", "")

        if sales.total_gmv:

            sales.total_gmv_value = (
                ParserUtils.money_to_float(
                    sales.total_gmv
                )
            )

        # -------------------------------------
        # Items Sold
        # -------------------------------------

        sales.items_sold = cards.get(
            "Items sold",
            ""
        )

        if sales.items_sold:

            sales.items_sold_value = (
                ParserUtils.count_to_int(
                    sales.items_sold
                )
            )

        # -------------------------------------
        # GPM
        # -------------------------------------

        sales.gpm = cards.get(
            "GPM",
            ""
        )

        if sales.gpm:

            sales.gpm_value = (
                ParserUtils.money_to_float(
                    sales.gpm
                )
            )

        # -------------------------------------
        # GMV per Customer
        # -------------------------------------

        sales.gmv_per_customer = cards.get(
            "GMV per customer",
            ""
        )

        if sales.gmv_per_customer:

            sales.gmv_per_customer_value = (
                ParserUtils.money_to_float(
                    sales.gmv_per_customer
                )
            )

        print("✓ Sales parsed")

    # ---------------------------------------------------------

    def wait_until_loaded(self):

        self.page.locator(
            "text=GMV per customer"
        ).wait_for(timeout=10000)