from playwright.sync_api import Page

from profiles.creator_profile import CreatorProfile

from profiles.header_parser import HeaderParser
from profiles.sales_parser import SalesParser
from profiles.collaboration_parser import CollaborationParser

from profiles.page_section_collector import PageSectionCollector


class ProfileExtractor:
    """
    Coordinates extraction of the complete creator profile.

    The page structure is discovered once, then each parser
    receives only the section it is responsible for parsing.
    """

    def __init__(self, page: Page):

        self.page = page

        self.header_parser = HeaderParser(page)

        self.sales_parser = SalesParser()

        self.collaboration_parser = CollaborationParser()

    # ---------------------------------------------------------

    def extract(self) -> CreatorProfile:

        print()
        print("=" * 60)
        print("Extracting Creator Profile")
        print("=" * 60)

        profile = CreatorProfile()

        # ---------------------------------------
        # Header
        # ---------------------------------------

        self.header_parser.parse(
            profile.header
        )

        # ---------------------------------------
        # Discover page sections
        # ---------------------------------------

        sections = PageSectionCollector(
            self.page
        ).collect()

        # ---------------------------------------
        # Sales
        # ---------------------------------------

        self.sales_parser.parse(
            sections.sales,
            profile.sales
        )

        # ---------------------------------------
        # Collaboration
        # ---------------------------------------

        self.collaboration_parser.parse(
            sections.collaboration,
            profile.collaboration
        )

        print("✓ Creator profile extracted.")

        return profile