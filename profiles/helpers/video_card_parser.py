from urllib.parse import urlparse, parse_qs

from playwright.sync_api import Locator, Page

from profiles.models.video_card_info import VideoCardInfo
from profiles.helpers.parser_utils import ParserUtils


class VideoCardParser:
    """
    Parses a single video card.

    Used by:
        - ExampleVideosParser
        - ProductVideosParser
    """

    def parse(
        self,
        card: Locator,
        page: Page
    ) -> VideoCardInfo:

        video = VideoCardInfo()

        # ---------------------------------------------------------
        # Thumbnail & Video ID
        # ---------------------------------------------------------

        image = card.locator(
            "img[alt='video thumbnail']"
        )

        if image.count():

            video.thumbnail_url = (
                image.first.get_attribute("src") or ""
            )

            if video.thumbnail_url:

                parsed_url = urlparse(
                    video.thumbnail_url
                )

                query_params = parse_qs(
                    parsed_url.query
                )

                video.video_id = (
                    query_params
                    .get("VideoID", [""])[0]
                )

        # ---------------------------------------------------------
        # Caption
        # ---------------------------------------------------------

        caption = card.locator(
            ".text-overflow-muli-2"
        )

        if caption.count():

            video.caption = (
                caption.first
                .inner_text()
                .strip()
            )

        # ---------------------------------------------------------
        # Release Time
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # Views & Likes
        # ---------------------------------------------------------

        metrics = card.locator(
            ".font-semibold"
        )

        metrics_count = metrics.count()

        if metrics_count >= 1:

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

        if metrics_count >= 2:

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

        # ---------------------------------------------------------
        # TikTok URL
        # ---------------------------------------------------------

        view_button = card.get_by_text(
            "View video on TikTok",
            exact=True
        )

        if view_button.count():

            try:

                with page.expect_popup(
                    timeout=5000
                ) as popup_info:

                    view_button.first.click()

                video_page = popup_info.value

                video.tiktok_url = video_page.url

                video_page.close()

            except Exception:

                video.tiktok_url = ""

        # ---------------------------------------------------------
        # Products
        # ---------------------------------------------------------

        video.has_products = (
            card.get_by_text(
                "View products",
                exact=True
            ).count() > 0
        )

        return video