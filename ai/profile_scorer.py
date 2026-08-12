from ai.scoring_context import ScoringContext


class ProfileScorer:
    """
    Calculates a deterministic profile-aware score
    for a creator against a campaign.

    This class does not call an AI/LLM.
    """

    @staticmethod
    def score(context: ScoringContext) -> float:

        scores = []

        # ---------------------------------------
        # Campaign Category Fit
        # ---------------------------------------

        category_score = (
            ProfileScorer._score_category_fit(
                context.profile_signals.campaign_category_gmv_percentage
            )
        )

        if category_score is not None:
            scores.append(
                (category_score, 25)
            )

        # ---------------------------------------
        # Product Video Performance
        # ---------------------------------------

        product_video_score = (
            ProfileScorer._score_product_video_performance(
                context.profile_signals.product_video_average_views,
                context.profile_signals.product_video_average_likes
            )
        )

        if product_video_score is not None:
            scores.append(
                (product_video_score, 20)
            )

        # ---------------------------------------
        # Content Type Sales Fit
        # ---------------------------------------

        content_type_score = (
            ProfileScorer._score_percentage(
                context.profile_signals
                .campaign_content_type_sales_percentage
            )
        )

        if content_type_score is not None:
            scores.append(
                (content_type_score, 15)
            )

        # ---------------------------------------
        # Brand Collaboration Experience
        # ---------------------------------------

        collaboration_score = (
            ProfileScorer._score_brand_collaborations(
                context.profile_signals.brand_collaborations
            )
        )

        if collaboration_score is not None:
            scores.append(
                (collaboration_score, 15)
            )

        # ---------------------------------------
        # Product Collaboration Volume
        # ---------------------------------------

        products_score = (
            ProfileScorer._score_products(
                context.profile_signals.products
            )
        )

        if products_score is not None:
            scores.append(
                (products_score, 10)
            )

        # ---------------------------------------
        # Commission
        # ---------------------------------------

        commission_score = (
            ProfileScorer._score_commission(
                context.profile_signals.average_commission_rate
            )
        )

        if commission_score is not None:
            scores.append(
                (commission_score, 5)
            )

        # ---------------------------------------
        # No usable profile signals
        # ---------------------------------------

        if not scores:
            return 0.0

        # ---------------------------------------
        # Normalize available weights
        # ---------------------------------------

        total_weight = sum(
            weight
            for _, weight in scores
        )

        weighted_score = sum(
            score * weight
            for score, weight in scores
        )

        return round(
            weighted_score / total_weight,
            2
        )

    # =====================================================
    # Category Fit
    # =====================================================

    @staticmethod
    def _score_category_fit(
        percentage: float | None
    ) -> float | None:

        if percentage is None:
            return None

        if percentage >= 80:
            return 100

        if percentage >= 60:
            return 90

        if percentage >= 40:
            return 75

        if percentage >= 20:
            return 60

        if percentage >= 10:
            return 40

        if percentage > 0:
            return 20

        return 0

    # =====================================================
    # Percentage Signal
    # =====================================================

    @staticmethod
    def _score_percentage(
        percentage: float | None
    ) -> float | None:

        if percentage is None:
            return None

        return max(
            0.0,
            min(
                float(percentage),
                100.0
            )
        )

    # =====================================================
    # Product Video Performance
    # =====================================================

    @staticmethod
    def _score_product_video_performance(
        average_views: float,
        average_likes: float
    ) -> float | None:

        if average_views <= 0 and average_likes <= 0:
            return None

        # ---------------------------------------
        # Views
        # ---------------------------------------

        if average_views >= 500_000:
            views_score = 100

        elif average_views >= 250_000:
            views_score = 90

        elif average_views >= 100_000:
            views_score = 80

        elif average_views >= 50_000:
            views_score = 65

        elif average_views >= 10_000:
            views_score = 50

        elif average_views >= 1_000:
            views_score = 30

        else:
            views_score = 10

        # ---------------------------------------
        # Likes
        # ---------------------------------------

        if average_likes >= 10_000:
            likes_score = 100

        elif average_likes >= 5_000:
            likes_score = 90

        elif average_likes >= 2_500:
            likes_score = 80

        elif average_likes >= 1_000:
            likes_score = 65

        elif average_likes >= 500:
            likes_score = 50

        elif average_likes >= 100:
            likes_score = 30

        else:
            likes_score = 10

        # ---------------------------------------
        # Combine
        # ---------------------------------------

        return round(
            (views_score * 0.70)
            + (likes_score * 0.30),
            2
        )

    # =====================================================
    # Brand Collaborations
    # =====================================================

    @staticmethod
    def _score_brand_collaborations(
        collaborations: int
    ) -> float | None:

        if collaborations <= 0:
            return 10

        if collaborations >= 50:
            return 100

        if collaborations >= 25:
            return 90

        if collaborations >= 10:
            return 80

        if collaborations >= 5:
            return 60

        if collaborations >= 2:
            return 40

        return 25

    # =====================================================
    # Products
    # =====================================================

    @staticmethod
    def _score_products(
        products: int
    ) -> float | None:

        if products <= 0:
            return 10

        if products >= 100:
            return 100

        if products >= 50:
            return 85

        if products >= 25:
            return 70

        if products >= 10:
            return 50

        if products >= 5:
            return 30

        return 20

    # =====================================================
    # Commission
    # =====================================================

    @staticmethod
    def _score_commission(
        commission: float
    ) -> float | None:

        if commission <= 0:
            return None

        if commission >= 15:
            return 100

        if commission >= 10:
            return 90

        if commission >= 7.5:
            return 80

        if commission >= 5:
            return 70

        if commission >= 3:
            return 50

        return 30