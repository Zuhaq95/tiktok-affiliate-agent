from playwright.sync_api import Locator

from creator import Creator


class CreatorParser:

    def parse(self, row: Locator) -> Creator:

        creator = Creator()

        cells = row.locator("td")
        creator_cell = cells.nth(1)

        # ---------------------------------
        # Username
        # ---------------------------------

        try:
            creator.username = creator_cell.locator(
                "span.text-body-m-medium"
            ).first.inner_text().strip()
        except:
            creator.username = ""

        # ---------------------------------
        # Display Name
        # ---------------------------------

        try:
            creator.name = creator_cell.locator(
                '[data-e2e="3b9caa65-c65a-e9df"]'
            ).first.inner_text().strip()
        except:
            creator.name = ""

        # ---------------------------------
        # Followers
        # ---------------------------------

        try:
            creator.followers = creator_cell.locator(
                '[data-e2e="7aed0dd7-48ba-6932"]'
            ).first.inner_text().strip()
        except:
            creator.followers = ""

        # ---------------------------------
        # Category
        # ---------------------------------

        try:
            category_text = creator_cell.locator(
                '[data-e2e="6e905dae-25bf-454b"]'
            ).first.inner_text().strip()

            creator.category = category_text

        except:
            creator.category = ""

        # ---------------------------------
        # Metrics
        # ---------------------------------

        try:
            creator.gmv = cells.nth(3).inner_text().strip()
        except:
            creator.gmv = ""

        try:
            creator.items_sold = cells.nth(4).inner_text().strip()
        except:
            creator.items_sold = ""

        try:
            creator.avg_views = cells.nth(5).inner_text().strip()
        except:
            creator.avg_views = ""

        try:
            creator.engagement = cells.nth(6).inner_text().strip()
        except:
            creator.engagement = ""

        # ---------------------------------
        # Invite Status
        # ---------------------------------

        try:
            invite_text = cells.nth(7).inner_text().strip()

            creator.previously_invited = (
                "Previously invited" in invite_text
                or "Invited" in invite_text
                or "Pending" in invite_text
            )

        except:
            creator.previously_invited = False

        return creator