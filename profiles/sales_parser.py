from playwright.sync_api import Page

from profiles.models.sales_info import SalesInfo


class SalesParser:
    """
    Parses the Sales tab.

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

        cards = self.metric_cards()

        sales.gmv = self.metric(cards.nth(0))
        sales.items_sold = self.metric(cards.nth(1))
        sales.gpm = self.metric(cards.nth(2))
        sales.gmv_per_customer = self.metric(cards.nth(3))

        print("✓ Sales parsed")

    # ---------------------------------------------------------

    def wait_until_loaded(self):

        self.page.locator(
            "text=GMV per customer"
        ).wait_for(timeout=10000)

    # ---------------------------------------------------------

    def metric_cards(self):

        return self.page.locator(
            "div.flex-1.min-w-0"
        )

    # ---------------------------------------------------------

    def metric(self, card):

        return (
            card
            .locator("span.text-head-l")
            .first
            .inner_text()
            .strip()
        )