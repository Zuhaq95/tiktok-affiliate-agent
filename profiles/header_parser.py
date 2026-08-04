from playwright.sync_api import Page
import re

from profiles.creator_profile import CreatorProfile


class HeaderParser:
    """
    Parses the creator header section.

    Extracts:
        - Username
        - Display Name
        - Rating
        - Review Count
        - Categories
        - Followers
        - MCN
        - Bio
        - Email
        - Website / Instagram
    """

    def __init__(self, page: Page):

        self.page = page

    # ---------------------------------------------------------

    def parse(self, profile: CreatorProfile):

        print("Parsing header...")

        self.wait_until_loaded()

        profile.username = self.username()
        profile.display_name = self.display_name()

        profile.rating = self.rating()
        profile.review_count = self.review_count()

        profile.categories = self.categories()
        profile.followers = self.followers()

        profile.mcn = self.mcn()

        profile.bio = self.bio()

        profile.email = self.email()

        profile.website = self.website()

        print("✓ Header parsed")

    # ---------------------------------------------------------

    def wait_until_loaded(self):

        self.page.locator(
            "button:has-text('Invite')"
        ).wait_for(timeout=10000)

    # ---------------------------------------------------------

    def username(self):

        return (
            self.page
            .locator("span.text-head-l")
            .first
            .inner_text()
            .strip()
        )
    
    # ---------------------------------------------------------

    def display_name(self):

        return (
            self.page
            .locator("span.text-overflow-single")
            .first
            .inner_text()
            .strip()
        )

        return ""

    # ---------------------------------------------------------

    def rating(self):

        text = self.page.locator("body").inner_text()

        match = re.search(
            r"Rating\s+([0-9.]+)",
            text
        )

        if match:

            return float(match.group(1))

        return None

    # ---------------------------------------------------------

    def review_count(self):

        text = self.page.locator("body").inner_text()

        match = re.search(
            r"(\d+)\s+review",
            text,
            re.IGNORECASE
        )

        if match:

            return int(match.group(1))

        return 0

    # ---------------------------------------------------------

    def categories(self):

        return self.value_after_label(
            "Categories"
        )

    # ---------------------------------------------------------

    def followers(self):

        return self.value_after_label(
            "Followers"
        )

    # ---------------------------------------------------------

    def mcn(self):

        return self.value_after_label(
            "MCN"
        )

    # ---------------------------------------------------------

    def bio(self):

        bio = self.page.locator(
            "span.whitespace-pre-wrap"
        )

        if bio.count():

            return bio.first.inner_text().strip()

        return ""

    # ---------------------------------------------------------

    def email(self):

        bio = self.bio()

        match = re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            bio
        )

        if match:

            return match.group(0)

        return ""

    # ---------------------------------------------------------

    def website(self):

        links = self.page.locator("a")

        if links.count():

            return (
                links.first
                .get_attribute("href")
            )

        return ""

    # ---------------------------------------------------------

    def value_after_label(self, label):

        spans = self.page.locator("span")

        count = spans.count()

        for i in range(count):

            text = spans.nth(i).inner_text().strip()

            if text == label:

                if i + 1 < count:

                    value = (
                        spans
                        .nth(i + 1)
                        .inner_text()
                    )

                    return " ".join(value.split())

        return ""