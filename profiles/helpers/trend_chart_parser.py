class TrendChartParser:
    """
    Parses a single creator profile trend record.

    TikTok returns trend data in the profile_types=[4]
    profile API response.

    This helper is responsible only for extracting the
    individual metric values from one stats record.
    """

    # ---------------------------------------------------------

    def parse(self, stats: dict) -> dict:

        

        profile = stats.get("profile", {})

        

        return {
            "gmv": self._parse_gmv(
                profile.get("trend_gmv")
            ),

            "units_sold": self._parse_value(
                profile.get("trend_units_sold")
            ),

            "followers": self._parse_value(
                profile.get("trend_follower")
            ),

            "video_views": self._parse_value(
                profile.get("trend_video_play_cnt")
            ),

            "engagement": self._parse_value(
                profile.get("trend_video_engagement_rate")
            ),
        }

    # ---------------------------------------------------------

    @staticmethod
    def _parse_value(metric: dict | None):

        if not metric:
            return None

        value = metric.get("value")

        if value is None:
            return None

        try:
            return float(value)

        except (TypeError, ValueError):
            return None

    # ---------------------------------------------------------

    @staticmethod
    def _parse_gmv(metric: dict | None):

        if not metric:
            return None

        value = metric.get("value")

        if not isinstance(value, dict):
            return None

        value = value.get("value")

        if value is None:
            return None

        try:
            return float(value)

        except (TypeError, ValueError):
            return None