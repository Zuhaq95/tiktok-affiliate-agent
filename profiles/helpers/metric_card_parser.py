from playwright.sync_api import Locator


class MetricCardParser:

    def __init__(self, section: Locator):

        self.section = section

    def parse(self) -> dict[str, str]:

        metrics = {}

        cards = self.section.locator(
            "div.flex-1.min-w-0"
        )

        for i in range(cards.count()):

            card = cards.nth(i)

            spans = card.locator("span")

            if spans.count() < 2:
                continue

            label = spans.first.inner_text().strip()

            value = spans.last.inner_text().strip()

            metrics[label] = value

        return metrics