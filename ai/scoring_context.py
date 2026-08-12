from dataclasses import dataclass, field

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

    product_video_average_views: float = 0.0

    product_video_average_likes: float = 0.0

    video_captions: list[str] = field(
        default_factory=list
    )

    product_video_captions: list[str] = field(
        default_factory=list
    )

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
        # Campaign category GMV fit
        # ---------------------------------------

        campaign_category_gmv_percentage = (
            ScoringContext._get_category_percentage(
                profile.sales.category_distribution,
                campaign.category
            )
        )

        # ---------------------------------------
        # Campaign content type / sales channel fit
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

            example_video_count=example_video_count,

            product_video_count=product_video_count,

            product_video_average_views=round(
                product_video_average_views,
                2
            ),

            product_video_average_likes=round(
                product_video_average_likes,
                2
            ),

            video_captions=video_captions,

            product_video_captions=(
                product_video_captions
            ),

            campaign_category_gmv_percentage=(
                campaign_category_gmv_percentage
            ),

            campaign_content_type_sales_percentage=(
                campaign_content_type_sales_percentage
            ),

            brand_collaborations=(
                brand_collaborations
            ),

            products=products,

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
    # Helpers
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
            except (TypeError, ValueError):
                continue

            if value < 0:
                continue

            values.append(value)

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
                    return float(percentage)
                except (TypeError, ValueError):
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
                    return float(percentage)
                except (TypeError, ValueError):
                    return None

        return None