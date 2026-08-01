from creator import Creator
from campaign import Campaign


class Scorer:
    """
    Calculates an AI score for a Creator.
    """

    @staticmethod
    def score(creator: Creator, campaign: Campaign) -> Creator:

        gmv_score = Scorer._score_gmv(creator.gmv_value)
        views_score = Scorer._score_views(creator.avg_views_value)
        engagement_score = Scorer._score_engagement(creator.engagement_value)
        followers_score = Scorer._score_followers(creator.followers_value)
        category_score = Scorer._score_category(
            creator.category,
            campaign.category
        )

        creator.ai_score = round(
            (gmv_score * 0.35)
            + (views_score * 0.25)
            + (engagement_score * 0.20)
            + (followers_score * 0.10)
            + (category_score * 0.10),
            2
        )

        return creator

    @staticmethod
    def _score_gmv(gmv: float) -> int:

        if gmv >= 200_000:
            return 100
        elif gmv >= 100_000:
            return 80
        elif gmv >= 50_000:
            return 60
        elif gmv >= 10_000:
            return 30
        return 10

    @staticmethod
    def _score_views(views: float) -> int:

        if views >= 100_000:
            return 100
        elif views >= 50_000:
            return 80
        elif views >= 10_000:
            return 60
        elif views >= 1_000:
            return 30
        return 10

    @staticmethod
    def _score_engagement(engagement: float) -> int:

        if engagement >= 8:
            return 100
        elif engagement >= 5:
            return 80
        elif engagement >= 3:
            return 60
        elif engagement >= 1:
            return 30
        return 10

    @staticmethod
    def _score_followers(followers: int) -> int:

        if followers >= 500_000:
            return 100
        elif followers >= 100_000:
            return 80
        elif followers >= 50_000:
            return 60
        elif followers >= 10_000:
            return 30
        return 10

    @staticmethod
    def _score_category(
        creator_category: str,
        campaign_category: str
    ) -> int:

        if creator_category.strip().lower() == campaign_category.strip().lower():
            return 100

        return 0