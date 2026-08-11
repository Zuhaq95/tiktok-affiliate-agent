from profiles.models.trend_info import TrendInfo
from profiles.helpers.trend_chart_parser import TrendChartParser


class TrendParser:
    """
    Parses creator trend data returned by TikTok's
    profile_types=[4] API response.

    The API structure is:

        creator_profile_trend_data
            └── stats
                └── profile
                    ├── trend_gmv
                    ├── trend_units_sold
                    ├── trend_follower
                    ├── trend_video_play_cnt
                    └── trend_video_engagement_rate
    """

    # ---------------------------------------------------------

    def __init__(self):

        self.chart_parser = TrendChartParser()

    # ---------------------------------------------------------

    def parse(
        self,
        trend_data,
        trends: TrendInfo
    ):

        print("Parsing trends...")

        if not trend_data:

            print("⚠ No trend API data available")

            return

        points = []

        # -----------------------------------------------------
        # creator_profile_trend_data
        # -----------------------------------------------------

        for trend_container in trend_data:

            if not isinstance(
                trend_container,
                dict
            ):
                continue

            stats = trend_container.get(
                "stats",
                []
            )

            if not isinstance(stats, list):
                continue

            # -------------------------------------------------
            # Daily trend points
            # -------------------------------------------------

            for stat in stats:

                if not isinstance(
                    stat,
                    dict
                ):
                    continue

                parsed = self.chart_parser.parse(
                    stat
                )

                print(
                    f"Trend point {len(points) + 1}: "
                    f"GMV={parsed['gmv']}, "
                    f"Units={parsed['units_sold']}, "
                    f"Followers={parsed['followers']}, "
                    f"Views={parsed['video_views']}, "
                    f"Engagement={parsed['engagement']}"
                )

                points.append(parsed)

        # -----------------------------------------------------
        # Convert parsed points into TrendInfo lists
        # -----------------------------------------------------

        trends.gmv_trend = [
            point["gmv"]
            for point in points
        ]

        trends.units_sold_trend = [
            point["units_sold"]
            for point in points
        ]

        trends.followers_trend = [
            point["followers"]
            for point in points
        ]

        trends.video_views_trend = [
            point["video_views"]
            for point in points
        ]

        trends.engagement_trend = [
            point["engagement"]
            for point in points
        ]

        print(
            f"✓ Parsed {len(points)} trend points"
        )