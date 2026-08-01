from playwright.sync_api import Page


class ProfileOpener:
    """
    Opens a creator profile in a new browser tab.

    Responsibilities:
        - Click a creator row
        - Wait for the popup tab
        - Return the newly opened profile page
    """

    def __init__(self, page: Page):
        self.page = page

    def open(self, creator_row) -> Page:

        print("Opening creator profile...")

        with self.page.expect_popup() as popup_info:
            creator_row.click()

        profile_page = popup_info.value

        profile_page.wait_for_load_state("domcontentloaded")

        print("✓ Creator profile opened")

        return profile_page