from playwright.sync_api import Page

from profiles.creator_profile import CreatorProfile

from profiles.header_parser import HeaderParser
from profiles.sales_parser import SalesParser
from profiles.collaboration_parser import CollaborationParser
from profiles.video_parser import VideoParser
from profiles.live_parser import LiveParser
from profiles.followers_parser import FollowersParser

from profiles.page_section_collector import PageSectionCollector
from profiles.example_videos_parser import ExampleVideosParser
from profiles.product_videos_parser import ProductVideosParser
from profiles.trend_parser import TrendParser


class ProfileExtractor:
    """
    Coordinates extraction of the complete creator profile.

    The page structure is discovered once, then each parser
    receives only the section it is responsible for parsing.
    """

    def __init__(
    self,
    page: Page,
    trend_data=None
    ):

        self.page = page

        self.trend_data = trend_data

        self.header_parser = HeaderParser(page)

        self.sales_parser = SalesParser()

        self.collaboration_parser = CollaborationParser()

        self.video_parser = VideoParser()

        self.live_parser = LiveParser()

        self.followers_parser = FollowersParser()

        self.trend_parser = TrendParser()

        self.example_videos_parser = ExampleVideosParser()

        self.product_videos_parser = ProductVideosParser()

        

    # ---------------------------------------------------------

    def extract(self) -> CreatorProfile:

        print()
        print("=" * 60)
        print("Extracting Creator Profile")
        print("=" * 60)

        profile = CreatorProfile()

        print(
            "Trend data records:",
            len(self.trend_data or [])
        )

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
            sections.sales_charts,
            profile.sales
        )

        # ---------------------------------------
        # Collaboration
        # ---------------------------------------

        self.collaboration_parser.parse(
            sections.collaboration,
            profile.collaboration
        )

        # ---------------------------------------
        # Video
        # ---------------------------------------

        self.video_parser.parse(
            sections.video,
            profile.videos
        )

        # ---------------------------------------
        # LIVE
        # ---------------------------------------

        self.live_parser.parse(
            sections.live,
            profile.live
        )
        # ---------------------------------------
                # followers
        # ---------------------------------------
        self.followers_parser.parse(
            sections.followers,
            profile.followers
        )
        # ---------------------------------------
        # trends
        # ---------------------------------------

        self.trend_parser.parse(
            self.trend_data,
            profile.trends
        )
        print()
        print("=" * 60)
        print("TREND DATA")
        print("=" * 60)

        print("GMV:")
        print(profile.trends.gmv_trend)

        print("Units Sold:")
        print(profile.trends.units_sold_trend)

        print("Followers:")
        print(profile.trends.followers_trend)

        print("Video Views:")
        print(profile.trends.video_views_trend)

        print("Engagement:")
        print(profile.trends.engagement_trend)


        # ---------------------------------------
                # example videos
        # ---------------------------------------


        profile.example_videos = (
        self.example_videos_parser.parse(
            sections.example_videos,
            self.page
        )
        )
        # ---------------------------------------
                        # Product  videos
        # ---------------------------------------

        profile.product_videos = (
        self.product_videos_parser.parse(
            sections.product_videos,
            self.page
        )
        )
        

        
        print("✓ Creator profile extracted.")

        return profile