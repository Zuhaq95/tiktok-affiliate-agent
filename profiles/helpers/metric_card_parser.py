from playwright.sync_api import Locator


class MetricCardParser:
    """
    Parses all visible metric cards inside a section.

    Responsibility:
        - Parse only the currently visible cards.
        - Never navigate the carousel.
    """

    CARD_SELECTOR = '[data-e2e="f6855061-9011-24ab"]'

    def __init__(self, section: Locator):
        self.section = section

    # ---------------------------------------------------------

    def parse_visible(self) -> dict[str, str]:

        metrics = {}

        cards = self.section.locator(self.CARD_SELECTOR)

        print(f"Found {cards.count()} visible metric cards")

        for i in range(cards.count()):

            card = cards.nth(i)

            try:

                label = (
                    card.locator("div")
                    .filter(has_text="")
                    .first
                )

                # Metric title
                title = (
                    card.locator("div")
                    .first
                    .inner_text()
                    .split("\n")[0]
                    .strip()
                )

                # Metric value
                value_locator = card.locator(".text-head-l")

                if value_locator.count() == 0:
                    continue

                value = value_locator.first.inner_text().strip()

                metrics[title] = value

                print(f"   {title} = {value}")

            except Exception as ex:

                print(f"Failed parsing metric card: {ex}")

        return metrics