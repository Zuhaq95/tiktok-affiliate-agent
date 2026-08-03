from playwright.sync_api import Page

from profiles.creator_profile import CreatorProfile


class CategoryParser:

    def __init__(self, page: Page):

        self.page = page

    def parse(self, profile: CreatorProfile):

        print("Parsing header...")

        profile.username = self.parse_username()

        profile.display_name = self.parse_display_name()

        profile.rating = self.parse_rating()

        profile.reviews = self.parse_reviews()

        profile.categories = self.parse_categories()

        profile.followers = self.parse_followers()

        profile.mcn = self.parse_mcn()

        profile.bio = self.parse_bio()

        print("✓ Header parsed")