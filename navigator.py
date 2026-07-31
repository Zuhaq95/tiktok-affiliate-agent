from config import DEBUG
from popup_handler import PopupHandler


class Navigator:

    def __init__(self, page):
        self.page = page
        self.popup_handler = PopupHandler(self.page)

    def open_discover_creators(self):

        # Open Affiliate Centre
        self.page.goto("https://affiliate.tiktok.com/")

        print("✓ Affiliate portal opened")

        # Close homepage popup if present
        self.popup_handler.close_startup_popup()

        # Locate Discover creators
        discover = self.page.get_by_text(
            "Discover creators",
            exact=True
        )

        discover.wait_for(timeout=30000)

        print("✓ Clicking Discover creators")

        discover.click()

        # Wait until we actually reach the creator page
        self.page.wait_for_url(
            "**/connection/creator*",
            timeout=30000
        )

        # Close popup if it appears after navigation
        self.popup_handler.close_startup_popup()

        # Wait until filters are available
        product_category = self.page.get_by_role(
            "button",
            name="Product category",
            exact=True
        )

        product_category.wait_for(timeout=30000)

        print("✓ Discover Creators page loaded")

        if DEBUG:
            print("🐞 Opening Playwright Inspector...")
            self.page.pause()