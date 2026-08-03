from playwright.sync_api import Page

from profiles.creator_result import CreatorResult


class ProfileOpener:
    """
    Opens a creator profile in a new browser tab.

    Responsibility:
        - Click creator row
        - Wait for popup tab
        - Return the newly opened page
    """

    def __init__(self, page: Page):

        self.page = page

    def open(self, result: CreatorResult) -> Page:

        print()
        print("=" * 50)
        print(f"Opening profile: {result.creator.username}")
        print("=" * 50)

        with self.page.expect_popup() as popup_info:

            result.row_locator.click()

        profile_page = popup_info.value

        profile_page.wait_for_load_state("domcontentloaded")

        print("✓ Profile opened successfully.")

        return profile_page