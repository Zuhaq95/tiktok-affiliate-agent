from playwright.sync_api import Page

from profiles.creator_profile import CreatorProfile
from profiles.header_parser import HeaderParser


class ProfileExtractor:
    """
    Coordinates extraction of the complete creator profile.

    Each parser is responsible for one section of the page.
    """

    def __init__(self, page: Page):

        self.page = page

    def extract(self) -> CreatorProfile:

        print()
        print("=" * 60)
        print("Extracting Creator Profile")
        print("=" * 60)

        profile = CreatorProfile()

        HeaderParser(
            self.page
        ).parse(profile)

        print("✓ Creator profile extracted.")

        return profile