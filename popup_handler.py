class PopupHandler:

    def __init__(self, page):
        self.page = page

    def close_startup_popup(self):

        try:

            button = self.page.get_by_role(
                "button",
                name="Close"
            )

            if button.count() > 0:

                print("✓ Startup popup detected")

                # Click outside the modal
                self.page.locator("body").click(
                    position={"x": 20, "y": 20},
                    force=True
                )

                self.page.wait_for_timeout(500)

                print("✓ Startup popup dismissed")

        except:
            pass