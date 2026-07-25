class DiscoveryPanel:

    def __init__(self, page):
        self.page = page

    def select_dropdown(self, button_name, option_text):

        print(f"Selecting {option_text}...")

        self.page.get_by_role(
            "button",
            name=button_name
        ).click()

        self.page.get_by_text(
            option_text
        ).click()

        print(f"✓ {option_text} selected")

    def apply_product_category(self, campaign):

        print("Applying Product Category...")

        self.select_dropdown(
            "Product category",
            campaign.category + " ("
        )

        self.page.get_by_text(
            campaign.subcategory
        ).click()

        print("✓ Product Category applied")