from creator import Creator
from ai.normalizer import Normalizer


class CreatorNormalizer:
    """
    Populates normalized numeric values on a Creator object.
    """

    @staticmethod
    def normalize(creator: Creator) -> Creator:

        creator.followers_value = Normalizer.followers(creator.followers)
        creator.gmv_value = Normalizer.gmv(creator.gmv)
        creator.items_sold_value = Normalizer.items_sold(creator.items_sold)
        creator.avg_views_value = Normalizer.avg_views(creator.avg_views)
        creator.engagement_value = Normalizer.engagement(creator.engagement)

        return creator