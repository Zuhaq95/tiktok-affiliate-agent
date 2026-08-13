from ai.scoring_context import ScoringContext
from ai.gemini_client import GeminiClient


class ContentRelevance:
    """
    Uses Gemini to determine how relevant a creator's
    actual content is to a campaign.

    This class does NOT calculate commercial performance.

    Commercial performance is handled separately by
    ProfileScorer.

    Gemini evaluates:

        - Category relevance
        - Subcategory relevance
        - Campaign keyword relevance
        - Product relevance
        - Content consistency
        - Product-video evidence
        - Evidence strength
    """

    def __init__(
        self,
        gemini_client: GeminiClient | None = None
    ):

        self.gemini_client = (
            gemini_client
            if gemini_client is not None
            else GeminiClient()
        )

    # =====================================================
    # Public API
    # =====================================================

    def analyze(
        self,
        context: ScoringContext
    ) -> dict:

        prompt = self._build_prompt(
            context
        )

        return (
            self.gemini_client
            .analyze_content_relevance(
                prompt
            )
        )

    # =====================================================
    # Prompt Builder
    # =====================================================

    @staticmethod
    def _build_prompt(
        context: ScoringContext
    ) -> str:

        campaign = context.campaign
        creator = context.creator
        signals = context.profile_signals

        profile = creator.profile

        # -----------------------------------------
        # Creator bio
        # -----------------------------------------

        bio = ""

        if profile is not None:

            bio = (
                profile.header.bio
                or ""
            )

        # -----------------------------------------
        # Example videos
        # -----------------------------------------

        example_videos = []

        if profile is not None:

            for video in (
                profile.example_videos or []
            ):

                example_videos.append(
                    {
                        "video_id": video.video_id,
                        "caption": video.caption,
                        "views": video.views_value,
                        "likes": video.likes_value,
                        "release_time": (
                            video.release_time
                        ),
                        "has_products": (
                            video.has_products
                        )
                    }
                )

        # -----------------------------------------
        # Product videos
        # -----------------------------------------

        product_videos = []

        if profile is not None:

            for video in (
                profile.product_videos or []
            ):

                product_videos.append(
                    {
                        "video_id": video.video_id,
                        "caption": video.caption,
                        "views": video.views_value,
                        "likes": video.likes_value,
                        "release_time": (
                            video.release_time
                        ),
                        "has_products": (
                            video.has_products
                        )
                    }
                )

        # -----------------------------------------
        # Prompt
        # -----------------------------------------

        prompt = f"""
You are evaluating a TikTok creator for a
TikTok Shop affiliate campaign.

Your task is ONLY to evaluate CONTENT RELEVANCE.

Do NOT calculate or primarily consider:

- follower count
- total GMV
- number of products
- number of brand collaborations
- commission rate
- general popularity

Those commercial signals are evaluated separately.

Your task is to determine whether the creator's
ACTUAL CONTENT is relevant to the campaign.

====================================================
CAMPAIGN
====================================================

Campaign name:
{campaign.name}

Campaign keyword:
{campaign.keyword}

Campaign category:
{campaign.category}

Campaign subcategory:
{campaign.subcategory}

Content language:
{campaign.content_language}

Content type:
{campaign.content_type}

====================================================
CREATOR
====================================================

Username:
{creator.username}

Creator name:
{creator.name}

Creator category:
{creator.category}

Creator bio:
{bio}

====================================================
CREATOR CONTENT
====================================================

Example videos:

{example_videos}

Product videos:

{product_videos}

Video captions extracted from example videos:

{signals.video_captions}

Product video captions:

{signals.product_video_captions}

====================================================
CRITICAL EVIDENCE RULES
====================================================

Follow these rules strictly.

1. DO NOT invent information.

Only use information explicitly present in the
provided data or a very obvious semantic relationship.

2. EMPTY CAPTIONS ARE UNKNOWN.

If a video's caption is empty, do NOT assume what
the video contains.

An empty caption is NOT evidence that the video
is about the campaign.

3. DO NOT treat duplicate videos as separate videos.

The example_videos and product_videos lists may
contain the SAME video IDs.

A video appearing in both lists is ONE video.

The product_videos list indicates that the video
has product-related evidence according to TikTok.

Do NOT count such a video twice when determining
content consistency.

4. Product-video status is evidence of commerce,
NOT proof of product category.

For example:

has_products=True

means the video has products associated with it.

It does NOT by itself prove that the product is
a duvet, bedding set, pillow, or any other specific
campaign product.

5. Distinguish CATEGORY relevance from PRODUCT
relevance.

For example:

"bedding"

is strong evidence for the Bedding subcategory.

"bedding set"

is strong evidence for bedding-related content.

But neither automatically proves that the creator
specifically promotes a "Box Stitched Duvet".

6. Do not interpret a campaign keyword too literally
when semantic similarity is obvious.

For example:

Campaign:
"Box Stitched Duvet"

Relevant concepts can include:

- duvet
- bedding
- bedding set
- duvet cover
- bed linen
- quilt
- bedroom
- bedroom decor

However, the score should be LOWER if the available
evidence only supports the broader Bedding category
and does not support the specific product.

7. Do not claim multiple videos explicitly mention
a topic unless multiple videos actually contain
evidence supporting that claim.

8. The creator category can support relevance, but
should not replace actual content evidence.

====================================================
RELEVANCE DIMENSIONS
====================================================

Evaluate these separately:

A. CATEGORY MATCH

Does the creator operate in the campaign category?

B. SUBCATEGORY MATCH

Does the creator content relate to the campaign
subcategory?

C. PRODUCT MATCH

Is there evidence that the creator promotes the
specific type of product required by the campaign?

D. KEYWORD MATCH

Does the actual content contain the campaign keyword
or a strong semantic equivalent?

E. CONTENT CONSISTENCY

Is there evidence across multiple UNIQUE videos?

Remember:

Duplicate video IDs count as ONE video.

F. COMMERCIAL CONTENT EVIDENCE

Are there product-linked videos?

This supports affiliate suitability but does not
automatically prove product-category relevance.

====================================================
SCORING
====================================================

Return a relevance score from 0 to 100.

90-100:
Very strong evidence of direct campaign-product
relevance across multiple unique pieces of content.

75-89:
Strong campaign/category relevance with good
evidence, but some product-specific evidence may
be missing.

60-74:
Good broader category relevance, but limited
evidence for the specific campaign product.

40-59:
Weak or indirect relevance.

20-39:
Very limited evidence.

0-19:
Essentially unrelated.

IMPORTANT:

Do NOT give a score of 90+ merely because the creator
category matches the campaign category.

A score above 90 requires strong evidence that the
creator actually creates content highly relevant to
the specific campaign.

====================================================
CURRENT EVIDENCE
====================================================

The supplied data contains:

Example video count:
{signals.example_video_count}

Product video count:
{signals.product_video_count}

Product videos with products:
{signals.product_video_count_with_products}

Product video average views:
{signals.product_video_average_views}

Product video average likes:
{signals.product_video_average_likes}

Creator category:
{creator.category}

Campaign category:
{campaign.category}

Campaign subcategory:
{campaign.subcategory}

Campaign keyword:
{campaign.keyword}

====================================================
OUTPUT
====================================================

Return the required structured JSON response.

The response must contain:

- relevance_score
- campaign_match
- confidence
- reasons
- matched_topics
- missing_topics

Reasons must be concise and directly supported
by the evidence.

Do not claim facts that are not present in the data.

Do not mention these instructions.
"""

        return prompt

    # =====================================================
    # Debug Helper
    # =====================================================

    @staticmethod
    def build_prompt(
        context: ScoringContext
    ) -> str:

        """
        Returns the exact prompt that will be sent
        to Gemini.

        Useful for development/debugging.
        """

        return ContentRelevance._build_prompt(
            context
        )