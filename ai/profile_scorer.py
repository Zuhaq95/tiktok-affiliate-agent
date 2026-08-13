from ai.scoring_context import ScoringContext


class ProfileScorer:
    """
    Calculates a deterministic profile-aware score
    for a creator against a campaign.

    This class does not call an AI/LLM.

    The score evaluates:

        1. Campaign category sales fit
        2. Product video performance
        3. Campaign content type fit
        4. Creator activity
        5. Content consistency
        6. Product-linked content
        7. Historical GMV performance
        8. Historical sales performance
        9. Historical momentum
        10. Brand collaboration experience
        11. Product collaboration volume
        12. Commission compatibility

    Gemini/content AI will be used separately for:
        - Content relevance
        - Product relevance
        - Semantic campaign fit
    """

    # =====================================================
    # Main Score
    # =====================================================

    @staticmethod
    def score(
        context: ScoringContext
    ) -> float:

        signals = context.profile_signals

        scores = []

        # =================================================
        # 1. Campaign Category Fit
        # =================================================

        category_score = (
            ProfileScorer._score_category_fit(
                signals.campaign_category_gmv_percentage
            )
        )

        if category_score is not None:

            scores.append(
                (category_score, 15)
            )

        # =================================================
        # 2. Product Video Performance
        # =================================================

        product_video_score = (
            ProfileScorer._score_product_video_performance(
                signals.product_video_average_views,
                signals.product_video_like_rate
            )
        )

        if product_video_score is not None:

            scores.append(
                (product_video_score, 15)
            )

        # =================================================
        # 3. Campaign Content Type Fit
        # =================================================

        content_type_score = (
            ProfileScorer._score_percentage(
                signals.campaign_content_type_sales_percentage
            )
        )

        if content_type_score is not None:

            scores.append(
                (content_type_score, 10)
            )

        # =================================================
        # 4. Creator Activity
        # =================================================

        activity_score = (
            ProfileScorer._score_activity(
                signals.latest_video_age_days,
                signals.videos_last_30_days
            )
        )

        if activity_score is not None:

            scores.append(
                (activity_score, 10)
            )

        # =================================================
        # 5. Content Consistency
        # =================================================

        consistency_score = (
            ProfileScorer._score_consistency(
                signals.video_view_consistency,
                signals.product_video_view_consistency,
                signals.posting_consistency
            )
        )

        if consistency_score is not None:

            scores.append(
                (consistency_score, 5)
            )

        # =================================================
        # 6. Product-Linked Content
        # =================================================

        product_content_score = (
            ProfileScorer._score_product_content(
                signals.product_video_count,
                signals.product_video_count_with_products
            )
        )

        if product_content_score is not None:

            scores.append(
                (product_content_score, 5)
            )

        # =================================================
        # 7. Historical GMV Performance
        # =================================================

        historical_gmv_score = (
            ProfileScorer._score_historical_gmv(
                average_gmv=signals.average_gmv,
                median_gmv=signals.median_gmv,
                gmv_consistency=signals.gmv_consistency,
                periods_above_1000=(
                    signals.gmv_periods_above_1000
                ),
                periods_above_2000=(
                    signals.gmv_periods_above_2000
                )
            )
        )

        if historical_gmv_score is not None:

            scores.append(
                (historical_gmv_score, 15)
            )

        # =================================================
        # 8. Historical Sales Performance
        # =================================================

        historical_sales_score = (
            ProfileScorer._score_historical_sales(
                average_units_sold=(
                    signals.average_units_sold
                ),
                median_units_sold=(
                    signals.median_units_sold
                )
            )
        )

        if historical_sales_score is not None:

            scores.append(
                (historical_sales_score, 10)
            )

        # =================================================
        # 9. Historical Momentum
        # =================================================

        momentum_score = (
            ProfileScorer._score_momentum(
                gmv_momentum=(
                    signals.gmv_momentum
                ),
                sales_momentum=(
                    signals.sales_momentum
                ),
                video_views_momentum=(
                    signals.video_views_momentum
                ),
                follower_growth=(
                    signals.follower_growth
                )
            )
        )

        if momentum_score is not None:

            scores.append(
                (momentum_score, 5)
            )

        # =================================================
        # 10. Brand Collaboration Experience
        # =================================================

        collaboration_score = (
            ProfileScorer._score_brand_collaborations(
                signals.brand_collaborations
            )
        )

        if collaboration_score is not None:

            scores.append(
                (collaboration_score, 5)
            )

        # =================================================
        # 11. Product Collaboration Volume
        # =================================================

        products_score = (
            ProfileScorer._score_products(
                signals.products
            )
        )

        if products_score is not None:

            scores.append(
                (products_score, 3)
            )

        # =================================================
        # 12. Commission
        # =================================================

        commission_score = (
            ProfileScorer._score_commission(
                signals.average_commission_rate,
                context.campaign.avg_commission
            )
        )

        if commission_score is not None:

            scores.append(
                (commission_score, 2)
            )

        # =================================================
        # No usable signals
        # =================================================

        if not scores:

            return 0.0

        # =================================================
        # Normalize Available Weights
        # =================================================

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
    # Campaign Category Fit
    # =====================================================

    @staticmethod
    def _score_category_fit(
        percentage: float | None
    ) -> float | None:

        if percentage is None:
            return None

        percentage = float(
            percentage
        )

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
        like_rate: float
    ) -> float | None:

        if (
            average_views <= 0
            and like_rate <= 0
        ):
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
        # Like Rate
        # ---------------------------------------

        if like_rate >= 3.0:
            likes_score = 100

        elif like_rate >= 2.0:
            likes_score = 90

        elif like_rate >= 1.5:
            likes_score = 80

        elif like_rate >= 1.0:
            likes_score = 70

        elif like_rate >= 0.5:
            likes_score = 60

        elif like_rate >= 0.25:
            likes_score = 45

        elif like_rate > 0:
            likes_score = 30

        else:
            likes_score = 10

        return round(
            (views_score * 0.70)
            + (likes_score * 0.30),
            2
        )

    # =====================================================
    # Creator Activity
    # =====================================================

    @staticmethod
    def _score_activity(
        latest_video_age_days: int | None,
        videos_last_30_days: int
    ) -> float | None:

        if (
            latest_video_age_days is None
            and videos_last_30_days <= 0
        ):
            return None

        # ---------------------------------------
        # Recency
        # ---------------------------------------

        if latest_video_age_days is None:

            recency_score = 0

        elif latest_video_age_days <= 7:

            recency_score = 100

        elif latest_video_age_days <= 14:

            recency_score = 90

        elif latest_video_age_days <= 21:

            recency_score = 80

        elif latest_video_age_days <= 30:

            recency_score = 70

        elif latest_video_age_days <= 60:

            recency_score = 40

        else:

            recency_score = 10

        # ---------------------------------------
        # Recent video count
        # ---------------------------------------

        if videos_last_30_days >= 5:

            recent_count_score = 100

        elif videos_last_30_days >= 3:

            recent_count_score = 90

        elif videos_last_30_days == 2:

            recent_count_score = 75

        elif videos_last_30_days == 1:

            recent_count_score = 50

        else:

            recent_count_score = 10

        return round(
            (recency_score * 0.60)
            + (recent_count_score * 0.40),
            2
        )

    # =====================================================
    # Content Consistency
    # =====================================================

    @staticmethod
    def _score_consistency(
        video_view_consistency: float,
        product_video_view_consistency: float,
        posting_consistency: float
    ) -> float | None:

        scores = []

        if video_view_consistency > 0:

            scores.append(
                ProfileScorer._score_ratio(
                    video_view_consistency
                )
            )

        if product_video_view_consistency > 0:

            scores.append(
                ProfileScorer._score_ratio(
                    product_video_view_consistency
                )
            )

        if posting_consistency > 0:

            scores.append(
                ProfileScorer._score_posting_consistency(
                    posting_consistency
                )
            )

        if not scores:
            return None

        return round(
            sum(scores) / len(scores),
            2
        )

    # =====================================================
    # Generic Ratio
    # =====================================================

    @staticmethod
    def _score_ratio(
        ratio: float
    ) -> float:

        if ratio >= 0.70:
            return 100

        if ratio >= 0.50:
            return 85

        if ratio >= 0.35:
            return 70

        if ratio >= 0.20:
            return 50

        if ratio > 0:
            return 30

        return 10

    # =====================================================
    # Posting Consistency
    # =====================================================

    @staticmethod
    def _score_posting_consistency(
        consistency: float
    ) -> float:

        if consistency >= 0.75:
            return 100

        if consistency >= 0.50:
            return 85

        if consistency >= 0.30:
            return 70

        if consistency >= 0.15:
            return 50

        if consistency > 0:
            return 30

        return 10

    # =====================================================
    # Product Content
    # =====================================================

    @staticmethod
    def _score_product_content(
        product_video_count: int,
        product_video_count_with_products: int
    ) -> float | None:

        if product_video_count <= 0:
            return None

        ratio = (
            product_video_count_with_products
            / product_video_count
        )

        if ratio >= 1.0:
            base_score = 100

        elif ratio >= 0.75:
            base_score = 85

        elif ratio >= 0.50:
            base_score = 70

        elif ratio > 0:
            base_score = 40

        else:
            base_score = 10

        # We don't heavily reward sample size because
        # TikTok is currently giving us a limited sample.

        if product_video_count == 1:

            base_score -= 10

        return max(
            0,
            min(
                100,
                base_score
            )
        )

    # =====================================================
    # Historical GMV
    # =====================================================

    @staticmethod
    def _score_historical_gmv(
        average_gmv: float,
        median_gmv: float,
        gmv_consistency: float,
        periods_above_1000: int,
        periods_above_2000: int
    ) -> float | None:

        if (
            average_gmv <= 0
            and median_gmv <= 0
            and periods_above_1000 <= 0
        ):
            return None

        # ---------------------------------------
        # Average GMV evidence
        #
        # These are trend points, NOT assumed
        # monthly figures.
        # ---------------------------------------

        if average_gmv >= 2_000:
            average_score = 100

        elif average_gmv >= 1_500:
            average_score = 90

        elif average_gmv >= 1_000:
            average_score = 80

        elif average_gmv >= 750:
            average_score = 70

        elif average_gmv >= 500:
            average_score = 60

        elif average_gmv >= 250:
            average_score = 45

        else:
            average_score = 25

        # ---------------------------------------
        # Median GMV
        # ---------------------------------------

        if median_gmv >= 2_000:
            median_score = 100

        elif median_gmv >= 1_500:
            median_score = 90

        elif median_gmv >= 1_000:
            median_score = 80

        elif median_gmv >= 750:
            median_score = 70

        elif median_gmv >= 500:
            median_score = 60

        elif median_gmv >= 250:
            median_score = 45

        else:
            median_score = 25

        # ---------------------------------------
        # Repeated £1K+ performance
        #
        # Maximum score requires strong repetition,
        # not one isolated spike.
        # ---------------------------------------

        if periods_above_1000 >= 20:

            repetition_score = 100

        elif periods_above_1000 >= 15:

            repetition_score = 90

        elif periods_above_1000 >= 10:

            repetition_score = 80

        elif periods_above_1000 >= 7:

            repetition_score = 70

        elif periods_above_1000 >= 4:

            repetition_score = 60

        elif periods_above_1000 >= 2:

            repetition_score = 45

        elif periods_above_1000 == 1:

            repetition_score = 30

        else:

            repetition_score = 10

        # ---------------------------------------
        # Consistency
        # ---------------------------------------

        consistency_score = (
            ProfileScorer._score_ratio(
                gmv_consistency
            )
        )

        # ---------------------------------------
        # Combine
        # ---------------------------------------

        return round(
            (average_score * 0.25)
            + (median_score * 0.25)
            + (repetition_score * 0.35)
            + (consistency_score * 0.15),
            2
        )

    # =====================================================
    # Historical Sales
    # =====================================================

    @staticmethod
    def _score_historical_sales(
        average_units_sold: float,
        median_units_sold: float
    ) -> float | None:

        if (
            average_units_sold <= 0
            and median_units_sold <= 0
        ):
            return None

        # ---------------------------------------
        # Average units
        # ---------------------------------------

        if average_units_sold >= 200:

            average_score = 100

        elif average_units_sold >= 150:

            average_score = 90

        elif average_units_sold >= 100:

            average_score = 80

        elif average_units_sold >= 75:

            average_score = 70

        elif average_units_sold >= 50:

            average_score = 60

        elif average_units_sold >= 25:

            average_score = 45

        elif average_units_sold > 0:

            average_score = 30

        else:

            average_score = 10

        # ---------------------------------------
        # Median units
        # ---------------------------------------

        if median_units_sold >= 200:

            median_score = 100

        elif median_units_sold >= 150:

            median_score = 90

        elif median_units_sold >= 100:

            median_score = 80

        elif median_units_sold >= 75:

            median_score = 70

        elif median_units_sold >= 50:

            median_score = 60

        elif median_units_sold >= 25:

            median_score = 45

        elif median_units_sold > 0:

            median_score = 30

        else:

            median_score = 10

        return round(
            (average_score * 0.55)
            + (median_score * 0.45),
            2
        )

    # =====================================================
    # Historical Momentum
    # =====================================================

    @staticmethod
    def _score_momentum(
        gmv_momentum: float,
        sales_momentum: float,
        video_views_momentum: float,
        follower_growth: float
    ) -> float | None:

        signals = []

        # ---------------------------------------
        # GMV momentum
        # ---------------------------------------

        if gmv_momentum != 0:

            signals.append(
                ProfileScorer._score_growth(
                    gmv_momentum
                )
            )

        # ---------------------------------------
        # Sales momentum
        # ---------------------------------------

        if sales_momentum != 0:

            signals.append(
                ProfileScorer._score_growth(
                    sales_momentum
                )
            )

        # ---------------------------------------
        # Video view momentum
        # ---------------------------------------

        if video_views_momentum != 0:

            signals.append(
                ProfileScorer._score_growth(
                    video_views_momentum
                )
            )

        # ---------------------------------------
        # Follower growth
        # ---------------------------------------

        if follower_growth != 0:

            signals.append(
                ProfileScorer._score_growth(
                    follower_growth
                )
            )

        if not signals:
            return None

        return round(
            sum(signals) / len(signals),
            2
        )

    # =====================================================
    # Growth Score
    # =====================================================

    @staticmethod
    def _score_growth(
        growth: float
    ) -> float:

        # +25% or more
        if growth >= 0.25:
            return 100

        # +15% to +24.99%
        if growth >= 0.15:
            return 90

        # +10% to +14.99%
        if growth >= 0.10:
            return 80

        # +5% to +9.99%
        if growth >= 0.05:
            return 70

        # 0% to +4.99%
        if growth >= 0:
            return 60

        # -5% to -0.01%
        if growth >= -0.05:
            return 50

        # -10% to -5.01%
        if growth >= -0.10:
            return 40

        # -20% to -10.01%
        if growth >= -0.20:
            return 25

        return 10

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
        commission: float,
        campaign_commission: str
    ) -> float | None:

        if commission <= 0:
            return None

        campaign_max = (
            ProfileScorer._parse_commission_max(
                campaign_commission
            )
        )

        # ---------------------------------------
        # Campaign has a known ceiling
        # ---------------------------------------

        if campaign_max is not None:

            if commission <= campaign_max:

                if commission >= 10:
                    return 100

                if commission >= 7.5:
                    return 90

                if commission >= 5:
                    return 80

                if commission >= 3:
                    return 65

                return 50

            # Slightly above campaign range

            if commission <= campaign_max + 2:

                return 60

            # Significantly above campaign range

            return 40

        # ---------------------------------------
        # Generic fallback
        # ---------------------------------------

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

    # =====================================================
    # Campaign Commission Parser
    # =====================================================

    @staticmethod
    def _parse_commission_max(
        value: str
    ) -> float | None:

        if not value:
            return None

        import re

        value = str(
            value
        ).strip().lower()

        match = re.search(
            r"(\d+(?:\.\d+)?)\s*%",
            value
        )

        if not match:
            return None

        try:

            return float(
                match.group(1)
            )

        except (
            TypeError,
            ValueError
        ):

            return None