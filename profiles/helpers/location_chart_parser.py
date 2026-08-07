from playwright.sync_api import Locator
class LocationChartParser:

    def __init__(self, section: Locator):
        self.section = section

    def parse(self) -> list[str]:

        print("Parsing Top 5 locations...")

        print(
            "⚠ Top 5 locations are rendered on a canvas "
            "and cannot be parsed using DOM selectors."
        )

        return []