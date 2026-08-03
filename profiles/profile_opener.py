from playwright.sync_api import Page, TimeoutError

from profiles.creator_result import CreatorResult


class ProfileOpener:
    """
    Opens a creator profile in a new browser tab.

    Responsibilities:
        - Click creator row
        - Wait for popup
        - Wait until Creator Details page is ready
        - Return the new page
    """

    def __init__(self, page: Page):

        self.page = page

    def open(self, result: CreatorResult) -> Page:

        print()
        print("=" * 60)
        print(f"Opening profile: {result.creator.username}")
        print("=" * 60)

        # Click row and wait for new tab
        with self.page.expect_popup() as popup_info:

            result.row_locator.scroll_into_view_if_needed()

            result.row_locator.click(timeout=10000)

        profile_page = popup_info.value

        # Wait for browser page
        profile_page.wait_for_load_state("domcontentloaded")
        profile_page.wait_for_load_state("networkidle")

        # Wait until Creator Details page is actually rendered
        self.wait_until_ready(profile_page)

        print("✓ Profile opened successfully.")

        return profile_page

    def wait_until_ready(self, profile_page: Page):

        """
        Wait until Creator Details page has finished rendering.
        """

        try:

            profile_page.locator(
                "text=Creator details"
            ).wait_for(timeout=10000)

            profile_page.locator("button:has-text('Invite')").wait_for()

        except TimeoutError:

            raise Exception(
                "Creator profile did not finish loading."
            )