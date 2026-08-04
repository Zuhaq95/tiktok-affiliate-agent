from playwright.sync_api import Page, TimeoutError

from profiles.creator_result import CreatorResult


class ProfileOpener:
    """
    Opens a creator profile in a new browser tab.

    Responsibilities:
        - Scroll creator row into view
        - Click creator row
        - Wait for popup tab
        - Wait until Creator Details page is rendered
        - Return the profile page
    """

    def __init__(self, page: Page):

        self.page = page

    def open(self, result: CreatorResult) -> Page:

        print()
        print("=" * 60)
        print(f"Opening profile: {result.creator.username}")
        print("=" * 60)

        # Click creator row and wait for new tab
        with self.page.expect_popup() as popup_info:

            result.row_locator.scroll_into_view_if_needed()

            result.row_locator.click(timeout=10000)

        profile_page = popup_info.value

        # Wait until browser DOM is ready
        profile_page.wait_for_load_state("domcontentloaded")

        # Wait until Creator Details page is rendered
        self.wait_until_ready(profile_page)

        print("✓ Profile opened successfully.")

        return profile_page

    def wait_until_ready(self, profile_page: Page):

        print("Waiting for 'Creator details'...")

        profile_page.locator(
            "text=Creator details"
        ).wait_for(timeout=20000)

        print("✓ Creator details found")

        print("Waiting for Invite button...")

        profile_page.locator(
            "button:has-text('Invite')"
        ).wait_for(timeout=20000)

        print("✓ Invite button found")