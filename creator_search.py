from playwright.sync_api import expect, TimeoutError


class CreatorSearch:

    def __init__(self, page):
        self.page = page

    def search(self, keyword):

        print(f"Searching for: {keyword}")

        search_box = self.page.get_by_role(
            "textbox",
            name="search names, products,"
        )

        expect(search_box).to_be_visible()

        search_box.click()

        search_box.fill("")
        search_box.fill(keyword)

        search_box.press("Enter")

        print("Waiting for search results...")

        # Wait for the request to finish.
        self.page.wait_for_load_state("networkidle")

        # Wait until at least one Invite button exists.
        try:
            self.page.wait_for_selector(
                'button:has-text("Invite")',
                timeout=30000
            )
        except TimeoutError:
            print("Invite button not found within timeout.")

        # Wait until there is more than one creator row.
        for _ in range(60):

            rows = self.page.locator("tbody tr").count()

            if rows > 1:
                print(f"✓ Results rendered ({rows} rows)")
                break

            self.page.wait_for_timeout(500)

        else:
            print("⚠ Only one row detected after waiting.")

        self.page.locator("body").click(position={"x": 5, "y": 5})

        print("✓ Search completed")