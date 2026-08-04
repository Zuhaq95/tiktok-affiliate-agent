from playwright.sync_api import Page


class MetricCardParser:
    """
    Parses metric cards that have the structure:

        Label
        Value

    Example:

        GMV
        £100.1K

    Returns:

        {
            "GMV": "£100.1K",
            "Items sold": "6.03K",
            ...
        }
    """

    def __init__(self, page: Page):

        self.page = page

    def parse(self) -> dict[str, str]:

        metrics = {}

        cards = self.page.locator(
            "div.flex-1.min-w-0"
        )

        print(f"\nMetric cards found : {cards.count()}")

        for i in range(cards.count()):

            card = cards.nth(i)

            try:

                label = (
                    card
                    .locator("div")
                    .first
                    .inner_text()
                    .strip()
                )

                value = (
                    card
                    .locator("span.text-head-l")
                    .first
                    .inner_text()
                    .strip()
                )

                metrics[label] = value

            except Exception:
                continue

        return metrics