from playwright.sync_api import Locator

from profiles.models.live_info import LiveInfo

from profiles.helpers.metric_card_parser import MetricCardParser
from profiles.helpers.carousel_navigator import CarouselNavigator
from profiles.helpers.parser_utils import ParserUtils


class LiveParser:
    """
    Parses the LIVE section.

    Responsibility:
        - Parse LIVE overview metrics
        - Parse LIVE carousel metrics

    It never searches the page.
    It only parses the section it is given.
    """

    # ---------------------------------------------------------

    def parse(
        self,
        section: Locator,
        live: LiveInfo
    ):

        print("Parsing LIVE...")

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

        print(f"✓ Parsed {len(metrics)} LIVE metrics")

        # ---------------------------------------
        # LIVE GPM
        # ---------------------------------------

        live.live_gpm = metrics.get(
            "LIVE GPM",
            ""
        )

        if live.live_gpm:

            live.live_gpm_value = (
                ParserUtils.money_to_float(
                    live.live_gpm
                )
            )

        # ---------------------------------------
        # LIVE Streams
        # ---------------------------------------

        live.live_streams = metrics.get(
            "LIVE streams",
            ""
        )

        if live.live_streams:

            live.live_streams_value = (
                ParserUtils.count_to_int(
                    live.live_streams
                )
            )

        # ---------------------------------------
        # Average LIVE Views
        # ---------------------------------------

        live.average_live_views = metrics.get(
            "Avg. LIVE views",
            ""
        )

        if live.average_live_views:

            live.average_live_views_value = (
                ParserUtils.count_to_int(
                    live.average_live_views
                )
            )

        # ---------------------------------------
        # Average Engagement Rate
        # ---------------------------------------

        live.average_live_engagement_rate = metrics.get(
            "Avg. LIVE engagement rate",
            ""
        )

        if live.average_live_engagement_rate:

            live.average_live_engagement_rate_value = (
                ParserUtils.percent_to_float(
                    live.average_live_engagement_rate
                )
            )

        # ---------------------------------------
        # Average Likes
        # ---------------------------------------

        live.average_live_likes = metrics.get(
            "Avg. LIVE likes",
            ""
        )

        if live.average_live_likes:

            live.average_live_likes_value = (
                ParserUtils.count_to_int(
                    live.average_live_likes
                )
            )

        # ---------------------------------------
        # Average Comments
        # ---------------------------------------

        live.average_live_comments = metrics.get(
            "Avg. LIVE comments",
            ""
        )

        if live.average_live_comments:

            live.average_live_comments_value = (
                ParserUtils.count_to_int(
                    live.average_live_comments
                )
            )

        # ---------------------------------------
        # Average Shares
        # ---------------------------------------

        live.average_live_shares = metrics.get(
            "Avg. LIVE shares",
            ""
        )

        if live.average_live_shares:

            live.average_live_shares_value = (
                ParserUtils.count_to_int(
                    live.average_live_shares
                )
            )

        print("✓ LIVE parsed")