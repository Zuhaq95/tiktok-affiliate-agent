from dataclasses import dataclass, field
from datetime import datetime
from statistics import median

from creator import Creator
from campaign import Campaign


@dataclass
class ProfileSignals:
    """
    Derived signals calculated from CreatorProfile data.

    These values are used by the scoring system.
    """

    # ---------------------------------------
    # Video content
    # ---------------------------------------

    example_video_count: int = 0

    product_video_count: int = 0

    product_video_count_with_products: int = 0

    product_video_average_views: float = 0.0

    product_video_average_likes: float = 0.0

    video_captions: list[str] = field(
        default_factory=list
    )

    product_video_captions: list[str] = field(
        default_factory=list
    )

    # ---------------------------------------
    # Activity
    # ---------------------------------------

    latest_video_age_days: int | None = None

    videos_last_30_days: int = 0

    # ---------------------------------------
    # View consistency
    # ---------------------------------------

    video_view_consistency: float = 0.0

    product_video_view_consistency: float = 0.0

    # ---------------------------------------
    # Video engagement
    # ---------------------------------------

    average_video_like_rate: float = 0.0

    product_video_like_rate: float = 0.0

    # ---------------------------------------
    # Posting consistency
    # ---------------------------------------

    average_days_between_videos: float = 0.0

    posting_consistency: float = 0.0

    # ---------------------------------------
    # Historical GMV
    # ---------------------------------------

    average_gmv: float = 0.0

    median_gmv: float = 0.0

    gmv_consistency: float = 0.0

    gmv_periods_above_1000: int = 0

    gmv_periods_above_2000: int = 0

    # ---------------------------------------
    # Historical Units Sold
    # ---------------------------------------

    average_units_sold: float = 0.0

    median_units_sold: float = 0.0

    # ---------------------------------------
    # Historical Video Views
    # ---------------------------------------

    average_trend_video_views: float = 0.0

    median_trend_video_views: float = 0.0

    # ---------------------------------------
    # Historical Growth
    # ---------------------------------------

    follower_growth: float = 0.0

    gmv_momentum: float = 0.0

    sales_momentum: float = 0.0

    video_views_momentum: float = 0.0

    # ---------------------------------------
    # Sales / Campaign Category Fit
    # ---------------------------------------

    campaign_category_gmv_percentage: float | None = None

    # ---------------------------------------
    # Sales Channel / Content Type Fit
    # ---------------------------------------

    campaign_content_type_sales_percentage: float | None = None

    # ---------------------------------------
    # Collaboration
    # ---------------------------------------

    brand_collaborations: int = 0

    products: int = 0

    average_commission_rate: float = 0.0


@dataclass
class ScoringContext:
    """
    Contains the information required to score a creator
    against a specific campaign.
    """

    creator: Creator

    campaign: Campaign

    profile_signals: ProfileSignals

    @property
    def profile(self):
        return self.creator.profile

    # =====================================================
    # Build Context
    # =====================================================

    @staticmethod
    def build(
        creator: Creator,
        campaign: Campaign
    ) -> "ScoringContext":

        profile = creator.profile

        # ---------------------------------------
        # No profile available
        # ---------------------------------------

        if profile is None:

            return ScoringContext(
                creator=creator,
                campaign=campaign,
                profile_signals=ProfileSignals()
            )

        # ---------------------------------------
        # Video signals
        # ---------------------------------------

        example_videos = (
            profile.example_videos or []
        )

        product_videos = (
            profile.product_videos or []
        )

        example_video_count = len(
            example_videos
        )

        product_video_count = len(
            product_videos
        )

        # ---------------------------------------
        # Product video metrics
        # ---------------------------------------

        product_video_average_views = (
            ScoringContext._average_video_metric(
                product_videos,
                "views_value"
            )
        )

        product_video_average_likes = (
            ScoringContext._average_video_metric(
                product_videos,
                "likes_value"
            )
        )

        # ---------------------------------------
        # Video captions
        # ---------------------------------------

        video_captions = (
            ScoringContext._extract_captions(
                example_videos
            )
        )

        product_video_captions = (
            ScoringContext._extract_captions(
                product_videos
            )
        )

        # ---------------------------------------
        # Product-linked videos
        # ---------------------------------------

        product_video_count_with_products = (
            ScoringContext._count_product_videos(
                product_videos
            )
        )

        # ---------------------------------------
        # Recent activity
        # ---------------------------------------

        latest_video_age_days = (
            ScoringContext._latest_video_age_days(
                example_videos
            )
        )

        videos_last_30_days = (
            ScoringContext._videos_last_n_days(
                example_videos,
                30
            )
        )

        # ---------------------------------------
        # View consistency
        # ---------------------------------------

        video_view_consistency = (
            ScoringContext._view_consistency(
                example_videos
            )
        )

        product_video_view_consistency = (
            ScoringContext._view_consistency(
                product_videos
            )
        )

        # ---------------------------------------
        # Like-rate signals
        # ---------------------------------------

        average_video_like_rate = (
            ScoringContext._average_like_rate(
                example_videos
            )
        )

        product_video_like_rate = (
            ScoringContext._average_like_rate(
                product_videos
            )
        )

        # ---------------------------------------
        # Posting consistency
        # ---------------------------------------

        average_days_between_videos = (
            ScoringContext._average_days_between_videos(
                example_videos
            )
        )

        posting_consistency = (
            ScoringContext._posting_consistency(
                example_videos
            )
        )

        # ---------------------------------------
        # Historical trend signals
        # ---------------------------------------

        trend_signals = (
            ScoringContext._build_trend_signals(
                profile
            )
        )

        # ---------------------------------------
        # Campaign category GMV fit
        # ---------------------------------------

        campaign_category_gmv_percentage = (
            ScoringContext._get_category_percentage(
                profile.sales.category_distribution,
                campaign.category
            )
        )

        # ---------------------------------------
        # Campaign content type / sales channel
        # ---------------------------------------

        campaign_content_type_sales_percentage = (
            ScoringContext._get_channel_percentage(
                profile.sales.sales_channel_distribution,
                campaign.content_type
            )
        )

        # ---------------------------------------
        # Collaboration signals
        # ---------------------------------------

        brand_collaborations = (
            profile.collaboration.brand_collaborations_value
        )

        products = (
            profile.collaboration.products_value
        )

        average_commission_rate = (
            profile.collaboration.average_commission_rate_value
        )

        # ---------------------------------------
        # Build signals
        # ---------------------------------------

        signals = ProfileSignals(

            # Video content
            example_video_count=(
                example_video_count
            ),

            product_video_count=(
                product_video_count
            ),

            product_video_count_with_products=(
                product_video_count_with_products
            ),

            product_video_average_views=round(
                product_video_average_views,
                2
            ),

            product_video_average_likes=round(
                product_video_average_likes,
                2
            ),

            video_captions=(
                video_captions
            ),

            product_video_captions=(
                product_video_captions
            ),

            # Activity
            latest_video_age_days=(
                latest_video_age_days
            ),

            videos_last_30_days=(
                videos_last_30_days
            ),

            # View consistency
            video_view_consistency=round(
                video_view_consistency,
                3
            ),

            product_video_view_consistency=round(
                product_video_view_consistency,
                3
            ),

            # Engagement
            average_video_like_rate=round(
                average_video_like_rate,
                3
            ),

            product_video_like_rate=round(
                product_video_like_rate,
                3
            ),

            # Posting consistency
            average_days_between_videos=round(
                average_days_between_videos,
                2
            ),

            posting_consistency=round(
                posting_consistency,
                3
            ),

            # Historical GMV
            average_gmv=round(
                trend_signals["average_gmv"],
                2
            ),

            median_gmv=round(
                trend_signals["median_gmv"],
                2
            ),

            gmv_consistency=round(
                trend_signals["gmv_consistency"],
                3
            ),

            gmv_periods_above_1000=(
                trend_signals[
                    "gmv_periods_above_1000"
                ]
            ),

            gmv_periods_above_2000=(
                trend_signals[
                    "gmv_periods_above_2000"
                ]
            ),

            # Historical units
            average_units_sold=round(
                trend_signals[
                    "average_units_sold"
                ],
                2
            ),

            median_units_sold=round(
                trend_signals[
                    "median_units_sold"
                ],
                2
            ),

            # Historical views
            average_trend_video_views=round(
                trend_signals[
                    "average_trend_video_views"
                ],
                2
            ),

            median_trend_video_views=round(
                trend_signals[
                    "median_trend_video_views"
                ],
                2
            ),

            # Historical growth
            follower_growth=round(
                trend_signals[
                    "follower_growth"
                ],
                4
            ),

            gmv_momentum=round(
                trend_signals[
                    "gmv_momentum"
                ],
                4
            ),

            sales_momentum=round(
                trend_signals[
                    "sales_momentum"
                ],
                4
            ),

            video_views_momentum=round(
                trend_signals[
                    "video_views_momentum"
                ],
                4
            ),

            # Campaign fit
            campaign_category_gmv_percentage=(
                campaign_category_gmv_percentage
            ),

            campaign_content_type_sales_percentage=(
                campaign_content_type_sales_percentage
            ),

            # Collaboration
            brand_collaborations=(
                brand_collaborations
            ),

            products=(
                products
            ),

            average_commission_rate=(
                average_commission_rate
            )
        )

        return ScoringContext(
            creator=creator,
            campaign=campaign,
            profile_signals=signals
        )

    # =====================================================
    # Video Helpers
    # =====================================================

    @staticmethod
    def _average_video_metric(
        videos,
        attribute_name: str
    ) -> float:

        if not videos:
            return 0.0

        values = []

        for video in videos:

            value = getattr(
                video,
                attribute_name,
                0
            )

            if value is None:
                continue

            try:
                value = float(value)

            except (
                TypeError,
                ValueError
            ):
                continue

            if value < 0:
                continue

            values.append(
                value
            )

        if not values:
            return 0.0

        return sum(values) / len(values)

    # =====================================================

    @staticmethod
    def _extract_captions(
        videos
    ) -> list[str]:

        captions = []

        for video in videos:

            caption = getattr(
                video,
                "caption",
                ""
            )

            if not caption:
                continue

            caption = str(
                caption
            ).strip()

            if not caption:
                continue

            captions.append(
                caption
            )

        return captions

    # =====================================================

    @staticmethod
    def _count_product_videos(
        videos
    ) -> int:

        if not videos:
            return 0

        count = 0

        for video in videos:

            has_products = getattr(
                video,
                "has_products",
                False
            )

            if has_products:
                count += 1

        return count

    # =====================================================
    # Date Helpers
    # =====================================================

    @staticmethod
    def _parse_release_date(
        value
    ) -> datetime | None:

        if not value:
            return None

        value = str(
            value
        ).strip()

        if not value:
            return None

        formats = [
            "%m.%d.%Y",
            "%m/%d/%Y",
            "%m-%d-%Y",
            "%Y.%m.%d",
            "%Y/%m/%d",
            "%Y-%m-%d",
        ]

        for date_format in formats:

            try:

                return datetime.strptime(
                    value,
                    date_format
                )

            except ValueError:
                continue

        return None

    # =====================================================

    @staticmethod
    def _get_video_dates(
        videos
    ) -> list[datetime]:

        dates = []

        if not videos:
            return dates

        for video in videos:

            release_time = getattr(
                video,
                "release_time",
                ""
            )

            parsed_date = (
                ScoringContext._parse_release_date(
                    release_time
                )
            )

            if parsed_date is None:
                continue

            dates.append(
                parsed_date
            )

        return sorted(
            dates
        )

    # =====================================================

    @staticmethod
    def _latest_video_age_days(
        videos
    ) -> int | None:

        dates = (
            ScoringContext._get_video_dates(
                videos
            )
        )

        if not dates:
            return None

        latest_date = max(
            dates
        )

        today = datetime.now().date()

        age = (
            today - latest_date.date()
        ).days

        if age < 0:
            return 0

        return age

    # =====================================================

    @staticmethod
    def _videos_last_n_days(
        videos,
        days: int
    ) -> int:

        dates = (
            ScoringContext._get_video_dates(
                videos
            )
        )

        if not dates:
            return 0

        today = datetime.now().date()

        count = 0

        for video_date in dates:

            age = (
                today - video_date.date()
            ).days

            if 0 <= age <= days:
                count += 1

        return count

    # =====================================================
    # Video Performance
    # =====================================================

    @staticmethod
    def _view_consistency(
        videos
    ) -> float:

        """
        Measures how consistently sampled videos perform.

        Formula:

            median views / maximum views

        Higher is better.
        """

        if not videos:
            return 0.0

        values = []

        for video in videos:

            value = getattr(
                video,
                "views_value",
                0
            )

            try:

                value = float(
                    value or 0
                )

            except (
                TypeError,
                ValueError
            ):

                continue

            if value <= 0:
                continue

            values.append(
                value
            )

        if not values:
            return 0.0

        maximum = max(
            values
        )

        if maximum <= 0:
            return 0.0

        return (
            median(values)
            / maximum
        )

    # =====================================================

    @staticmethod
    def _average_like_rate(
        videos
    ) -> float:

        if not videos:
            return 0.0

        rates = []

        for video in videos:

            views = getattr(
                video,
                "views_value",
                0
            )

            likes = getattr(
                video,
                "likes_value",
                0
            )

            try:

                views = float(
                    views or 0
                )

                likes = float(
                    likes or 0
                )

            except (
                TypeError,
                ValueError
            ):

                continue

            if views <= 0:
                continue

            if likes < 0:
                continue

            rate = (
                likes / views
            ) * 100

            rates.append(
                rate
            )

        if not rates:
            return 0.0

        return (
            sum(rates)
            / len(rates)
        )

    # =====================================================

    @staticmethod
    def _average_days_between_videos(
        videos
    ) -> float:

        dates = (
            ScoringContext._get_video_dates(
                videos
            )
        )

        if len(dates) < 2:
            return 0.0

        intervals = []

        for index in range(
            1,
            len(dates)
        ):

            difference = (
                dates[index].date()
                - dates[index - 1].date()
            ).days

            if difference >= 0:
                intervals.append(
                    difference
                )

        if not intervals:
            return 0.0

        return (
            sum(intervals)
            / len(intervals)
        )

    # =====================================================

    @staticmethod
    def _posting_consistency(
        videos
    ) -> float:

        """
        Estimates posting consistency from the
        sampled video dates.

        A value closer to 1.0 means the intervals
        are more similar.

        Fewer than three dated videos are not
        enough evidence for this signal.
        """

        dates = (
            ScoringContext._get_video_dates(
                videos
            )
        )

        if len(dates) < 3:
            return 0.0

        intervals = []

        for index in range(
            1,
            len(dates)
        ):

            difference = (
                dates[index].date()
                - dates[index - 1].date()
            ).days

            if difference > 0:
                intervals.append(
                    difference
                )

        if len(intervals) < 2:
            return 0.0

        minimum_interval = min(
            intervals
        )

        maximum_interval = max(
            intervals
        )

        if maximum_interval <= 0:
            return 0.0

        return (
            minimum_interval
            / maximum_interval
        )

    # =====================================================
    # Historical Trend Signals
    # =====================================================

    @staticmethod
    def _build_trend_signals(
        profile
    ) -> dict:

        """
        Builds derived signals from the trend arrays
        captured from TikTok.

        Important:

        We do not assume that one trend point equals
        one specific calendar period. The extractor
        currently gives us ordered trend points, so
        momentum is calculated by comparing the older
        half of the available points with the newer half.
        """

        trends = profile.trends

        gmv_values = (
            ScoringContext._clean_numeric_values(
                trends.gmv_trend
            )
        )

        units_values = (
            ScoringContext._clean_numeric_values(
                trends.units_sold_trend
            )
        )

        follower_values = (
            ScoringContext._clean_numeric_values(
                trends.followers_trend
            )
        )

        video_view_values = (
            ScoringContext._clean_numeric_values(
                trends.video_views_trend
            )
        )

        # ---------------------------------------
        # GMV
        # ---------------------------------------

        average_gmv = (
            ScoringContext._average(
                gmv_values
            )
        )

        median_gmv = (
            ScoringContext._median(
                gmv_values
            )
        )

        gmv_consistency = (
            ScoringContext._trend_consistency(
                gmv_values
            )
        )

        gmv_periods_above_1000 = sum(
            1
            for value in gmv_values
            if value >= 1_000
        )

        gmv_periods_above_2000 = sum(
            1
            for value in gmv_values
            if value >= 2_000
        )

        # ---------------------------------------
        # Units Sold
        # ---------------------------------------

        average_units_sold = (
            ScoringContext._average(
                units_values
            )
        )

        median_units_sold = (
            ScoringContext._median(
                units_values
            )
        )

        # ---------------------------------------
        # Historical Video Views
        # ---------------------------------------

        average_trend_video_views = (
            ScoringContext._average(
                video_view_values
            )
        )

        median_trend_video_views = (
            ScoringContext._median(
                video_view_values
            )
        )

        # ---------------------------------------
        # Follower Growth
        #
        # Percentage change from first available
        # point to last available point.
        # ---------------------------------------

        follower_growth = (
            ScoringContext._percentage_change(
                follower_values[0],
                follower_values[-1]
            )
            if len(follower_values) >= 2
            else 0.0
        )

        # ---------------------------------------
        # GMV Momentum
        # ---------------------------------------

        gmv_momentum = (
            ScoringContext._half_momentum(
                gmv_values
            )
        )

        # ---------------------------------------
        # Sales Momentum
        # ---------------------------------------

        sales_momentum = (
            ScoringContext._half_momentum(
                units_values
            )
        )

        # ---------------------------------------
        # Video View Momentum
        # ---------------------------------------

        video_views_momentum = (
            ScoringContext._half_momentum(
                video_view_values
            )
        )

        return {
            "average_gmv": average_gmv,

            "median_gmv": median_gmv,

            "gmv_consistency": gmv_consistency,

            "gmv_periods_above_1000": (
                gmv_periods_above_1000
            ),

            "gmv_periods_above_2000": (
                gmv_periods_above_2000
            ),

            "average_units_sold": (
                average_units_sold
            ),

            "median_units_sold": (
                median_units_sold
            ),

            "average_trend_video_views": (
                average_trend_video_views
            ),

            "median_trend_video_views": (
                median_trend_video_views
            ),

            "follower_growth": (
                follower_growth
            ),

            "gmv_momentum": (
                gmv_momentum
            ),

            "sales_momentum": (
                sales_momentum
            ),

            "video_views_momentum": (
                video_views_momentum
            )
        }

    # =====================================================

    @staticmethod
    def _clean_numeric_values(
        values
    ) -> list[float]:

        if not values:
            return []

        cleaned = []

        for value in values:

            if value is None:
                continue

            try:

                numeric_value = float(
                    value
                )

            except (
                TypeError,
                ValueError
            ):

                continue

            if numeric_value < 0:
                continue

            cleaned.append(
                numeric_value
            )

        return cleaned

    # =====================================================

    @staticmethod
    def _average(
        values: list[float]
    ) -> float:

        if not values:
            return 0.0

        return (
            sum(values)
            / len(values)
        )

    # =====================================================

    @staticmethod
    def _median(
        values: list[float]
    ) -> float:

        if not values:
            return 0.0

        return float(
            median(values)
        )

    # =====================================================

    @staticmethod
    def _trend_consistency(
        values: list[float]
    ) -> float:

        """
        Measures how consistently the trend performs.

        Formula:

            median / maximum

        Higher means the creator's performance is
        less dependent on isolated spikes.
        """

        if not values:
            return 0.0

        maximum = max(
            values
        )

        if maximum <= 0:
            return 0.0

        median_value = median(
            values
        )

        return (
            median_value
            / maximum
        )

    # =====================================================

    @staticmethod
    def _percentage_change(
        first: float,
        last: float
    ) -> float:

        if first <= 0:
            return 0.0

        return (
            (last - first)
            / first
        )

    # =====================================================

    @staticmethod
    def _half_momentum(
        values: list[float]
    ) -> float:

        """
        Compares the newer half of the trend with
        the older half.

        Formula:

            newer average / older average - 1

        Example:

            older average = 500
            newer average = 750

            momentum = 0.50

        Meaning:

            +50% improvement.
        """

        if len(values) < 4:
            return 0.0

        midpoint = len(values) // 2

        older = values[
            :midpoint
        ]

        newer = values[
            midpoint:
        ]

        if not older or not newer:
            return 0.0

        older_average = (
            ScoringContext._average(
                older
            )
        )

        newer_average = (
            ScoringContext._average(
                newer
            )
        )

        if older_average <= 0:
            return 0.0

        return (
            newer_average
            / older_average
        ) - 1.0

    # =====================================================
    # Campaign Fit
    # =====================================================

    @staticmethod
    def _get_category_percentage(
        distribution: dict[str, float],
        campaign_category: str
    ) -> float | None:

        if not distribution:
            return None

        target = (
            campaign_category.strip().lower()
        )

        for category, percentage in distribution.items():

            if category.strip().lower() == target:

                try:

                    return float(
                        percentage
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    return None

        return None

    # =====================================================

    @staticmethod
    def _get_channel_percentage(
        distribution: dict[str, float],
        campaign_content_type: str
    ) -> float | None:

        if not distribution:
            return None

        target = (
            campaign_content_type.strip().lower()
        )

        for channel, percentage in distribution.items():

            if channel.strip().lower() == target:

                try:

                    return float(
                        percentage
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    return None

        return None