from playwright.sync_api import Locator


class DistributionParser:
    """
    Parses donut chart legends.

    Supported charts:

        - GMV per sales channel
        - GMV by product category
        - Gender
        - Age
    """

    def __init__(self, section: Locator):

        self.section = section

    # ---------------------------------------------------------

    def parse(
        self,
        title: str
    ) -> dict[str, float]:

        print()
        print(f"Parsing distribution: {title}")

        distributions = {}

        heading = self.section.get_by_text(
            title,
            exact=True
        )

        if heading.count() == 0:

            print(f"✗ '{title}' not found")

            return distributions

        # -----------------------------------------------------
        # Locate the chart container
        # -----------------------------------------------------

        container = heading.first.locator(
            "xpath=ancestor::div[contains(@class,'pcm-pc-container')]"
        )

        if container.count() == 0:

            print("✗ Chart container not found")

            return distributions

        # -----------------------------------------------------
        # Legend labels
        # -----------------------------------------------------

        labels = container.locator(
            ".pcm-pc-legend-label .ecom-data-overflow-text-content"
        )

        # -----------------------------------------------------
        # Legend values
        # -----------------------------------------------------

        values = container.locator(
            ".pcm-pc-legend-value .ecom-data-overflow-text-content"
        )

        print(
            f"Found {labels.count()} labels and {values.count()} values"
        )

        count = min(
            labels.count(),
            values.count()
        )

        for i in range(count):

            label = labels.nth(i).inner_text().strip()

            value = values.nth(i).inner_text().strip()

            try:

                percent = float(
                    value.replace("%", "")
                )

                distributions[label] = percent

                print(
                    f"   {label} = {percent}%"
                )

            except ValueError:

                continue

        return distributions