from playwright.sync_api import Locator

from profiles.models.followers_info import FollowersInfo

from profiles.helpers.distribution_parser import DistributionParser
from profiles.helpers.location_chart_parser import LocationChartParser



class FollowersParser:
    """
    Parses the Followers section.

    Responsibility

        - Gender distribution
        - Age distribution
        - Top 5 locations

    It never searches the page.

    It only parses the section it is given.
    """

    # ---------------------------------------------------------

    def parse(
        self,
        section: Locator,
        followers: FollowersInfo
    ):

        print("Parsing followers...")

        distribution_parser = DistributionParser(
            section
        )

        # ---------------------------------------
        # Gender
        # ---------------------------------------

        followers.gender_distribution = (
            distribution_parser.parse(
                "Gender"
            )
        )

        print(
            f"✓ Parsed {len(followers.gender_distribution)} gender entries"
        )

        # ---------------------------------------
        # Age
        # ---------------------------------------

        followers.age_distribution = (
            distribution_parser.parse(
                "Age"
            )
        )

        print(
            f"✓ Parsed {len(followers.age_distribution)} age entries"
        )

        # ---------------------------------------
        # Locations
        # ---------------------------------------

        followers.top_locations = (
            LocationChartParser(
                section
            ).parse()
        )

        print(
            f"✓ Parsed {len(followers.top_locations)} locations"
        )

        print("✓ Followers parsed")