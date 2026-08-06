from playwright.sync_api import Locator


class DistributionParser:
    """
    Parses donut chart legends.

    Example:
        GMV per sales channel
        GMV by product category
        Gender
        Age
    """

    def __init__(self, section: Locator):

        self.section = section

    # ---------------------------------------------------------

    def parse(self, title: str) -> dict[str, float]:

        distributions = {}

        # Find the chart container by its title
        chart = (
            self.section
            .locator(f"text={title}")
            .locator("..")
        )

        spans = chart.locator("span")

        texts = []

        for i in range(spans.count()):

            value = spans.nth(i).inner_text().strip()

            if value:
                texts.append(value)

        # Legend usually appears as:
        # Video
        # 93.41%
        # LIVE
        # 6.59%

        i = 0

        while i < len(texts) - 1:

            label = texts[i]

            value = texts[i + 1]

            if value.endswith("%"):

                try:

                    distributions[label] = float(
                        value.replace("%", "")
                    )

                    i += 2
                    continue

                except ValueError:
                    pass

            i += 1

        return distributions