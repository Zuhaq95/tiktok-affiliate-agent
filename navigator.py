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

        PopupHandler(self.page).close_startup_popup()

        input("STEP 1 - Is the Affiliate homepage fully loaded? Press ENTER...")

        discover = self.page.get_by_text("Discover creators")

        print("✓ Clicking Discover creators")

        discover.click()

        self.page.wait_for_load_state("networkidle")
        PopupHandler(self.page).close_startup_popup()

        input("STEP 2 - Did the page actually change? Press ENTER...")

        if DEBUG:
            print("🐞 Opening Playwright Inspector...")
            self.page.pause()