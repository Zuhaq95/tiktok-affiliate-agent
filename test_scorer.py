from creator import Creator
from campaign import Campaign

from ai.creator_normalizer import CreatorNormalizer
from ai.scorer import Scorer


creator = Creator(
    username="creator1",
    followers="11.7K",
    gmv="£174K",
    items_sold="8.1K",
    avg_views="35K",
    engagement="4%",
    category="Textiles & Soft Furnishings"
)

campaign = Campaign(
    name="Test Campaign",
    keyword="Bedsheet",
    category="Textiles & Soft Furnishings",
    subcategory="Bedding",
    content_language="English",
    gmv="100K",
    avg_commission="15%",
    content_type="Video",
    not_invited=True
)

CreatorNormalizer.normalize(creator)

Scorer.score(creator, campaign)

print(f"AI Score: {creator.ai_score}")