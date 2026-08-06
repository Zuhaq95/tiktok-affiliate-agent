from playwright.sync_api import Locator


class CarouselNavigator:
    """
    Handles horizontal carousel navigation.

    Responsibility:
        - Detect next arrow
        - Click next
        - Wait for carousel animation

    Never parses any business data.
    """

    NEXT_ARROW = "svg.alliance-icon-ArrowRight"

    def __init__(self, section: Locator):
        self.section = section

    # ---------------------------------------------------------

    def has_next(self) -> bool:

        arrow = self.section.locator(self.NEXT_ARROW)

        return (
            arrow.count() > 0
            and arrow.first.is_visible()
        )

    # ---------------------------------------------------------

    def move_next(self) -> bool:

        if not self.has_next():

            print("✓ End of carousel")

            return False

        print("→ Moving carousel")

        self.section.locator(
            self.NEXT_ARROW
        ).first.click()

        # TikTok carousel animation
        self.section.page.wait_for_timeout(350)

        return True