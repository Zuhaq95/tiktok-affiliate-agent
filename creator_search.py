from playwright.sync_api import Page


class CreatorSearch:

    def __init__(self, page: Page):
        self.page = page

    def search(self, creator_name: str):

        search_box = self.page.get_by_role(
            "textbox",
            name="search names, products,"
        )

        search_box.fill(creator_name)

        search_box.press("Enter")