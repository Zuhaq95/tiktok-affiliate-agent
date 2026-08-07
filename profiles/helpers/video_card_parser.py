from playwright.sync_api import Locator

from profiles.models.video_card_info import VideoCardInfo
from profiles.helpers.parser_utils import ParserUtils


class VideoCardParser:
    """
    Parses a single video card.

    Used by

        - ExampleVideosParser
        - ProductVideosParser
    """

    # ---------------------------------------------------------

    def parse(
        self,
        card: Locator
    ) -> VideoCardInfo:

        video = VideoCardInfo()

        # ---------------------------------------
        # Thumbnail
        # ---------------------------------------

        image = card.locator(
            "img[alt='video thumbnail']"
        )

        if image.count():

            video.thumbnail_url = (
                image.get_attribute("src") or ""
            )

        # ---------------------------------------
        # Caption
        # ---------------------------------------

        caption = card.locator(
            ".text-overflow-muli-2"
        )

        if caption.count():

            video.caption = (
                caption.first.inner_text().strip()
            )

        # ---------------------------------------
        # Release Time
        # ---------------------------------------

        release = card.locator(
            "text=Release Time:"
        )

        if release.count():

            video.release_time = (
                release.first
                .inner_text()
                .replace(
                    "Release Time:",
                    ""
                )
                .strip()
            )

        # ---------------------------------------
        # Views
        # ---------------------------------------

        metrics = card.locator(
            ".font-semibold"
        )

        if metrics.count() >= 1:

            video.views = (
                metrics.nth(0)
                .inner_text()
                .strip()
            )

            video.views_value = (
                ParserUtils.count_to_int(
                    video.views
                )
            )

        # ---------------------------------------
        # Likes
        # ---------------------------------------

        if metrics.count() >= 2:

            video.likes = (
                metrics.nth(1)
                .inner_text()
                .strip()
            )

            video.likes_value = (
                ParserUtils.count_to_int(
                    video.likes
                )
            )

        # ---------------------------------------
        # TikTok Link
        # ---------------------------------------

        links = card.locator("a")

        if links.count():

            video.tiktok_url = (
                links.first.get_attribute("href")
                or ""
            )

        # ---------------------------------------
        # Products Button
        # ---------------------------------------

        video.has_products = (
            card.get_by_text(
                "View products"
            ).count() > 0
        )

        return video