from playwright.sync_api import Locator
import re


class DistributionParser:
    """
    Parses chart legends like:

    Video      93.41%
    LIVE       6.59%

    or

    Textiles & Soft Furnishings   40.37%
    Other                         28.06%
    """

    def __init__(self, container: Locator):

        self.container = container

    def parse(self) -> dict[str, float]:

        distribution = {}

        text = self.container.inner_text()

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            match = re.match(
                r"(.+?)\s+([\d.]+)%$",
                line
            )

            if not match:
                continue

            label = match.group(1).strip()

            percentage = float(
                match.group(2)
            )

            distribution[label] = percentage

        return distribution