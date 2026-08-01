from creator import Creator
from campaign import Campaign


class Recommender:
    """
    Generates human-readable explanations for a creator's AI score.
    """

    @staticmethod
    def recommend(creator: Creator, campaign: Campaign) -> Creator:

        reasons = []

        # ------------------------
        # GMV
        # ------------------------
        if creator.gmv_value >= 200000:
            reasons.append(f"Excellent GMV ({creator.gmv})")
        elif creator.gmv_value >= 100000:
            reasons.append(f"Strong GMV ({creator.gmv})")
        elif creator.gmv_value < 10000:
            reasons.append(f"Low GMV ({creator.gmv})")

        # ------------------------
        # Average Views
        # ------------------------
        if creator.avg_views_value >= 100000:
            reasons.append(f"Excellent average views ({creator.avg_views})")
        elif creator.avg_views_value >= 50000:
            reasons.append(f"Strong average views ({creator.avg_views})")
        elif creator.avg_views_value < 1000:
            reasons.append(f"Low average views ({creator.avg_views})")

        # ------------------------
        # Engagement
        # ------------------------
        if creator.engagement_value >= 8:
            reasons.append(f"Outstanding engagement ({creator.engagement})")
        elif creator.engagement_value >= 5:
            reasons.append(f"Strong engagement ({creator.engagement})")
        elif creator.engagement_value < 1:
            reasons.append(f"Low engagement ({creator.engagement})")

        # ------------------------
        # Followers
        # ------------------------
        if creator.followers_value >= 500000:
            reasons.append(
                f"Large follower base ({creator.followers})"
            )
        elif creator.followers_value >= 100000:
            reasons.append(
                f"Strong follower base ({creator.followers})"
            )
        elif creator.followers_value < 10000:
            reasons.append(
                f"Growing audience ({creator.followers})"
            )

        # NOTE:
        # We intentionally do NOT compare creator.category with
        # campaign.category.
        #
        # TikTok already filters creators by the selected campaign
        # category, while the table only displays the creator's
        # primary category. A creator may actively sell products
        # in multiple categories that are not shown here.
        #
        # In Phase 2 this will be replaced with real evidence from
        # the creator profile (Revenue by Category).

        creator.ai_reasons = reasons

        return creator