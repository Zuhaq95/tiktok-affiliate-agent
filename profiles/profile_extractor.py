from playwright.sync_api import Page

from profiles.creator_profile import CreatorProfile

from profiles.sales_parser import SalesParser
from profiles.video_parser import VideoParser
from profiles.followers_parser import FollowerParser
from profiles.trend_parser import TrendParser
from profiles.header_parser import CategoryParser


class ProfileExtractor:

    def __init__(self, page: Page):

        self.page = page

    def extract(self) -> CreatorProfile:

        print()
        print("=" * 60)
        print("Extracting Creator Profile")
        print("=" * 60)

        profile = CreatorProfile()

        profile.sales = SalesParser(
            self.page
        ).parse()

        profile.video = VideoParser(
            self.page
        ).parse()

        profile.followers = FollowerParser(
            self.page
        ).parse()

        profile.trends = TrendParser(
            self.page
        ).parse()

        profile.categories = CategoryParser(
            self.page
        ).parse()

        print("✓ Profile extracted")

        return profile