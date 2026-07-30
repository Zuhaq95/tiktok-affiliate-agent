from config import DEBUG
from popup_handler import PopupHandler


class Navigator:

    def __init__(self, page):
        self.page = page
        self.popup_handler = PopupHandler(self.page)

    def open_discover_creators(self):

        self.page.goto(
            "https://affiliate.tiktok.com/",
            wait_until="domcontentloaded"
        )

        self.page.wait_for_load_state("networkidle")

        print("✓ Affiliate portal opened")

        # Close homepage popup if present
        self.popup_handler.close_startup_popup()

        # Wait until Discover creators is available
        discover = self.page.get_by_text("Discover creators")
        discover.wait_for(state="visible", timeout=15000)

        print("✓ Clicking Discover creators")

        discover.click()

        # Wait for next page to finish loading
        self.page.wait_for_load_state("networkidle")

        # Close starter pack popup if it appears
        self.popup_handler.close_startup_popup()

        # Wait until filters become available
        self.page.get_by_role(
            "button",
            name="Product category"
        ).wait_for(
            state="visible",
            timeout=15000
        )

        print("✓ Discover Creators page loaded")

        if DEBUG:
            print("🐞 Opening Playwright Inspector...")
            self.page.pause()