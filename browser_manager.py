from playwright.sync_api import sync_playwright


class BrowserManager:

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir="sessions/tiktok",
            headless= False 
        )


        if self.browser.pages:
            self.page = self.browser.pages[0]
        else:
            self.page = self.browser.new_page()

        self.page.set_default_timeout(60000)

        return self.page

    def stop(self):

        self.browser.close()

        self.playwright.stop()