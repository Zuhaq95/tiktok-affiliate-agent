from playwright.sync_api import Locator, Page

from profiles.page_sections import PageSections


class PageSectionCollector:
    """
    Discovers every major section on the Creator Details page.
    """

    EXPECTED_SECTION_COUNT = 11

    def __init__(self, page: Page):

        self.page = page

    # ---------------------------------------------------------

    def collect(self) -> PageSections:

        cards = self.page.locator("div.bg-white")

        count = cards.count()

        print()
        print("=" * 60)
        print("Collecting Page Sections")
        print("=" * 60)
        print(f"Found {count} white sections")

        if count < self.EXPECTED_SECTION_COUNT:

            raise RuntimeError(
                f"""
Expected at least {self.EXPECTED_SECTION_COUNT} sections.

Found {count}.

TikTok page layout may have changed.
"""
            )

        sections = PageSections(

            header=cards.nth(0),

            navigation=cards.nth(1),

            sales=cards.nth(2),

            sales_charts=cards.nth(3),

            collaboration=cards.nth(4),

            video=cards.nth(5),

            live=cards.nth(6),

            followers=cards.nth(7),

            trends=cards.nth(8),

            example_videos=cards.nth(9),

            product_videos=cards.nth(10),
        )

        self.validate(sections)

        print("✓ Page sections collected")

        return sections

    # ---------------------------------------------------------

    def validate(
        self,
        sections: PageSections
    ):

        self.assert_contains(
            sections.sales,
            "Sales"
        )

        self.assert_contains(
            sections.collaboration,
            "Collaboration metrics"
        )

        self.assert_contains(
            sections.video,
            "Video"
        )

        self.assert_contains(
            sections.live,
            "LIVE"
        )

        self.assert_contains(
            sections.followers,
            "Followers"
        )

        self.assert_contains(
            sections.trends,
            "TRENDS"
        )

        self.assert_contains(
            sections.example_videos,
            "Videos"
        )

        self.assert_contains(
            sections.product_videos,
            "Videos with product"
        )

    # ---------------------------------------------------------

    def assert_contains(
        self,
        section: Locator,
        expected: str
    ):

        text = section.inner_text()

        if expected not in text:

            raise RuntimeError(
                f"""
Expected section containing:

    {expected}

Instead found:

{text[:300]}
"""
            )