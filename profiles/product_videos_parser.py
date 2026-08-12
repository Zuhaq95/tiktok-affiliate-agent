from playwright.sync_api import Locator, Page

from profiles.models.video_card_info import VideoCardInfo

from profiles.helpers.video_card_parser import VideoCardParser


class ProductVideosParser:
    """
    Parses the Videos with Product section.

    Responsibility:

        - Find every product video card
        - Parse each card using VideoCardParser

    It never searches the page.

    It only parses the section it is given.
    """

    # ---------------------------------------------------------

    def parse(
        self,
        section: Locator,
        page: Page
    ) -> list[VideoCardInfo]:

        print("Parsing product videos...")

        parser = VideoCardParser()

        videos = []

        cards = (
            section
            .locator(".core-spin-children")
            .locator("> div.flex")
        )

        print(f"Found {cards.count()} video cards")

        for i in range(cards.count()):

            print(f"Parsing card {i + 1}")

            video = parser.parse(
                cards.nth(i),
                page
            )

            videos.append(video)

            print(
                f"   Caption : {video.caption[:50]}"
            )

            print(
                f"   Views   : {video.views}"
            )

            print(
                f"   Likes   : {video.likes}"
            )

            print(
                f"   TikTok URL : {video.tiktok_url}"
            )

        print(
            f"✓ Parsed {len(videos)} product videos"
        )

        return videos