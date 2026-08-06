from playwright.sync_api import Page

from profiles.creator_profile import CreatorProfile

from profiles.header_parser import HeaderParser
from profiles.sales_parser import SalesParser
from profiles.collaboration_parser import CollaborationParser


class ProfileExtractor:
    """
    Coordinates extraction of the complete creator profile.

    Each parser is responsible for one section of the page.
    """

    def __init__(self, page: Page):

        self.page = page

        self.header_parser = HeaderParser(page)
        self.sales_parser = SalesParser(page)
        self.collaboration_parser = CollaborationParser(page)

    def extract(self) -> CreatorProfile:

        print()
        print("=" * 60)
        print("Extracting Creator Profile")
        print("=" * 60)

        profile = CreatorProfile()

        # -------------------------------
        # Header
        # -------------------------------

        self.header_parser.parse(
            profile.header
        )

        # -------------------------------
        # Sales
        # -------------------------------

        self.sales_parser.parse(
            profile.sales
        )

        # -------------------------------
        # Collaboration
        # -------------------------------

        self.collaboration_parser.parse(
            profile.collaboration
        )

        print("✓ Creator profile extracted.")

        return profile