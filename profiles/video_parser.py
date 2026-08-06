from playwright.sync_api import Locator

from profiles.models.video_info import VideoInfo

from profiles.helpers.metric_card_parser import MetricCardParser
from profiles.helpers.carousel_navigator import CarouselNavigator
from profiles.helpers.parser_utils import ParserUtils


class VideoParser:
    """
    Parses the Video section.

    Responsibility:
        - Parse video overview metrics
        - Parse carousel metrics

    It never searches the page.
    It only parses the section it is given.
    """

    # ---------------------------------------------------------

    def parse(
        self,
        section: Locator,
        video: VideoInfo
    ):

        print("Parsing video...")

        metric_parser = MetricCardParser(section)
        navigator = CarouselNavigator(section)

        metrics = {}

        # ---------------------------------------
        # Metric Cards
        # ---------------------------------------

        metrics.update(
            metric_parser.parse_visible()
        )

        while navigator.move_next():

            metrics.update(
                metric_parser.parse_visible()
            )

        print(f"✓ Parsed {len(metrics)} video metrics")

        # ---------------------------------------
        # Video GPM
        # ---------------------------------------

        video.video_gpm = metrics.get(
            "Video GPM",
            ""
        )

        if video.video_gpm:

            video.video_gpm_value = (
                ParserUtils.money_to_float(
                    video.video_gpm
                )
            )

        # ---------------------------------------
        # Videos
        # ---------------------------------------

        video.videos = metrics.get(
            "Videos",
            ""
        )

        if video.videos:

            video.videos_value = (
                ParserUtils.count_to_int(
                    video.videos
                )
            )

        # ---------------------------------------
        # Average Video Views
        # ---------------------------------------

        video.average_video_views = metrics.get(
            "Avg. video views",
            ""
        )

        if video.average_video_views:

            video.average_video_views_value = (
                ParserUtils.count_to_int(
                    video.average_video_views
                )
            )

        # ---------------------------------------
        # Average Engagement Rate
        # ---------------------------------------

        video.average_video_engagement_rate = metrics.get(
            "Avg. video engagement rate",
            ""
        )

        if video.average_video_engagement_rate:

            video.average_video_engagement_rate_value = (
                ParserUtils.percent_to_float(
                    video.average_video_engagement_rate
                )
            )

        # ---------------------------------------
        # Average Likes
        # ---------------------------------------

        video.average_video_likes = metrics.get(
            "Avg. video likes",
            ""
        )

        if video.average_video_likes:

            video.average_video_likes_value = (
                ParserUtils.count_to_int(
                    video.average_video_likes
                )
            )

        # ---------------------------------------
        # Average Comments
        # ---------------------------------------

        video.average_video_comments = metrics.get(
            "Avg. video comments",
            ""
        )

        if video.average_video_comments:

            video.average_video_comments_value = (
                ParserUtils.count_to_int(
                    video.average_video_comments
                )
            )

        # ---------------------------------------
        # Average Shares
        # ---------------------------------------

        video.average_video_shares = metrics.get(
            "Avg. video shares",
            ""
        )

        if video.average_video_shares:

            video.average_video_shares_value = (
                ParserUtils.count_to_int(
                    video.average_video_shares
                )
            )

        print("✓ Video parsed")