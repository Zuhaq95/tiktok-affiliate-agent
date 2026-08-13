from playwright.sync_api import expect, TimeoutError


class CreatorSearch:

    def __init__(self, page):
        self.page = page

    def search(self, keyword):

        print(
            f"Searching for: {keyword}"
        )

        # ----------------------------------------
        # Find search box
        # ----------------------------------------

        search_box = self.page.get_by_role(
            "textbox",
            name="search names, products,"
        )

        expect(
            search_box
        ).to_be_visible(
            timeout=10000
        )

        # ----------------------------------------
        # Enter search keyword
        # ----------------------------------------

        search_box.click()

        search_box.fill("")

        search_box.fill(
            keyword
        )

        # ----------------------------------------
        # Submit search
        # ----------------------------------------

        search_box.press(
            "Enter"
        )

        print(
            "Waiting for search results..."
        )

        # ----------------------------------------
        # Wait for creator rows
        #
        # IMPORTANT:
        # Do NOT use networkidle here.
        #
        # TikTok may continue background
        # network requests even after the
        # search results have rendered.
        # ----------------------------------------

        rows = self.page.locator(
            "tbody tr"
        )

        try:

            expect(
                rows.first
            ).to_be_visible(
                timeout=30000
            )

        except TimeoutError:

            print(
                "❌ Creator rows did not appear "
                "within 30 seconds."
            )

            # ------------------------------------
            # Diagnostic information
            # ------------------------------------

            try:

                print(
                    "Current URL:",
                    self.page.url
                )

            except Exception:
                pass

            try:

                print(
                    "Search box value:",
                    search_box.input_value()
                )

            except Exception:
                pass

            try:

                print(
                    "Current row count:",
                    rows.count()
                )

            except Exception:
                pass

            raise

        # ----------------------------------------
        # Give the table a short moment to finish
        # rendering additional rows.
        # ----------------------------------------

        self.page.wait_for_timeout(
            1000
        )

        row_count = rows.count()

        print(
            f"✓ Results rendered ({row_count} rows)"
        )

        # ----------------------------------------
        # Wait briefly for Invite buttons if they
        # are part of the creator rows.
        #
        # This is NOT required for search
        # completion.
        # ----------------------------------------

        invite_buttons = self.page.locator(
            'button:has-text("Invite")'
        )

        try:

            expect(
                invite_buttons.first
            ).to_be_visible(
                timeout=5000
            )

            print(
                "✓ Invite buttons rendered"
            )

        except TimeoutError:

            print(
                "⚠ Invite buttons not visible yet."
            )

        # ----------------------------------------
        # Remove focus from search box
        # ----------------------------------------

        try:

            self.page.locator(
                "body"
            ).click(
                position={
                    "x": 5,
                    "y": 5
                }
            )

        except Exception:
            pass

        print(
            "✓ Search completed"
        )