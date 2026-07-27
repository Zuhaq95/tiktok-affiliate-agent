from config import DEBUG
class Navigator:

    def __init__(self, page):
        self.page = page

    def open_discover_creators(self, debug=False):

        #self.page.goto("https://affiliate.tiktok.com/")
        self.page.goto(
    "https://affiliate.tiktok.com/",
    wait_until="domcontentloaded"
)

        print("✓ Affiliate portal opened")

        input("STEP 1 - Is the Affiliate homepage fully loaded? Press ENTER...")

        discover = self.page.get_by_text("Discover creators")

        print("✓ Clicking Discover creators")

        discover.click()

        input("STEP 2 - Did the page actually change? Press ENTER...")

        if DEBUG:
            print("🐞 Opening Playwright Inspector...")
            self.page.pause()