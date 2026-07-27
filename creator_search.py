from playwright.sync_api import expect


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

        self.page.wait_for_load_state("networkidle")

        print("✓ Search completed")