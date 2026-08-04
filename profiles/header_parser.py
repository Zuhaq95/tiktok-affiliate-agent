from playwright.sync_api import Page

from profiles.creator_profile import CreatorProfile


class HeaderParser:
    """
    Parses the top creator information section.

    This parser extracts everything above the Sales tabs.

    Responsibility:
        - username
        - display name
        - categories
        - followers
        - rating
        - reviews
        - MCN
        - bio
        - email
        - website / Instagram
    """

    def __init__(self, page: Page):

        self.page = page

    def parse(self, profile: CreatorProfile):

        print("Parsing header...")

        self.wait_until_loaded()

        profile.username = self.username()
        profile.display_name = self.display_name()
        profile.categories = self.categories()
        profile.followers = self.followers()

        # We'll implement these one-by-one
        profile.rating = None
        profile.review_count = None
        profile.mcn = None
        profile.bio = None
        profile.email = None
        profile.website = None

        print("✓ Header parsed")

    # -------------------------------------------------

    def wait_until_loaded(self):

        self.page.locator(
            "button:has-text('Invite')"
        ).wait_for()

    # -------------------------------------------------

    def username(self):

        return (
            self.page
            .locator("span.leading-21")
            .first
            .inner_text()
            .strip()
        )

    # -------------------------------------------------

    def display_name(self):

        return (
            self.page
            .locator("span.leading-21")
            .nth(1)
            .inner_text()
            .strip()
        )

    # -------------------------------------------------

    def categories(self):

        labels = self.page.locator("span")

        count = labels.count()

        for i in range(count):

            text = labels.nth(i).inner_text().strip()

            if text == "Categories":

                return (
                    labels
                    .nth(i + 1)
                    .inner_text()
                    .strip()
                )

        return ""

    # -------------------------------------------------

    def followers(self):

        labels = self.page.locator("span")

        count = labels.count()

        for i in range(count):

            text = labels.nth(i).inner_text().strip()

            if text == "Followers":

                return (
                    labels
                    .nth(i + 1)
                    .inner_text()
                    .strip()
                )

        return ""