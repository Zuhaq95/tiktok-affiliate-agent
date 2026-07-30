from popup_handler import PopupHandler


class DiscoveryPanel:

    def __init__(self, page):
        self.page = page
        self.popup_handler = PopupHandler(self.page)

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

        self.popup_handler.close_startup_popup()

        self.select_dropdown(
            "Product category",
            campaign.category + " ("
        )

        self.page.get_by_text(
            campaign.subcategory
        ).click()

        print("✓ Product Category applied")

    def apply_filters(self, campaign):

        print("\n========== APPLYING FILTERS ==========\n")

        self.apply_product_category(campaign)

        self.apply_content_type(campaign)

        print("\n✓ Filters applied\n")

    def select_radio_dropdown(self, button_name, option_text):

        print(f"Selecting {button_name}: {option_text}")

        self.page.get_by_role(
        "button",
        name=button_name,
        exact=True
         ).click()

        popup = self.page.locator("[id^='core-select-popup-']").last

        popup.get_by_text(
            option_text,
            exact=True
        ).click()

        print(f"✓ {button_name} selected")
    def apply_content_type(self, campaign):

        print("Applying Content Type...")

        self.select_radio_dropdown(
            "Content type",
            campaign.content_type
        )

        print("✓ Content Type applied")