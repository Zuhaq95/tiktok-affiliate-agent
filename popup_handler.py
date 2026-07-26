class PopupHandler:

    def __init__(self, page):
        self.page = page

    def close_startup_popup(self):

        try:
            button = self.page.get_by_role(
                "button",
                name="Close"
            )

            if button.first.is_visible():
                button.first.click()
                print("✓ Startup popup closed")

        except:
            pass