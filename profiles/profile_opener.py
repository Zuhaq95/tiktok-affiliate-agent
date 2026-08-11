import json

from playwright.sync_api import Page

from profiles.creator_result import CreatorResult


class ProfileOpener:
    """
    Opens a creator profile in a new browser tab.

    Responsibilities:
        - Scroll creator row into view
        - Click creator row
        - Wait for popup tab
        - Capture creator profile API responses
        - Wait until Creator Details page is rendered
        - Return the profile page
    """

    def __init__(self, page: Page):

        self.page = page

        # Raw trend API response
        self.trend_data = None

    # ---------------------------------------------------------

    def open(self, result: CreatorResult) -> Page:

        print()
        print("=" * 60)
        print(f"Opening profile: {result.creator.username}")
        print("=" * 60)

        # ---------------------------------------
        # Start listening BEFORE opening profile
        # ---------------------------------------

        self.page.context.on(
            "response",
            self._handle_response
        )

        # ---------------------------------------
        # Click creator row and wait for new tab
        # ---------------------------------------

        with self.page.expect_popup() as popup_info:

            result.row_locator.scroll_into_view_if_needed()

            result.row_locator.click(
                timeout=10000
            )

        profile_page = popup_info.value

        # ---------------------------------------
        # Wait until browser DOM is ready
        # ---------------------------------------

        profile_page.wait_for_load_state(
            "domcontentloaded"
        )

        # ---------------------------------------
        # Wait until Creator Details page
        # ---------------------------------------

        self.wait_until_ready(
            profile_page
        )

        print("✓ Profile opened successfully.")

        if self.trend_data is not None:

            print("✓ Trend API data captured")

        else:

            print("⚠ Trend API data was not captured")

        return profile_page

    # ---------------------------------------------------------

    def _handle_response(self, response):

        try:

            # ---------------------------------------
            # Only marketplace profile endpoint
            # ---------------------------------------

            if "/api/v1/oec/affiliate/creator/marketplace/profile" not in response.url:
                return

            request = response.request

            # ---------------------------------------
            # Only POST
            # ---------------------------------------

            if request.method != "POST":
                return

            post_data = request.post_data

            if not post_data:
                return

            payload = json.loads(post_data)

            # ---------------------------------------
            # Only profile type 4
            # ---------------------------------------

            profile_types = payload.get(
                "profile_types"
            )

            if profile_types != [4]:
                return

            print()
            print("✓ Found profile type [4] request")

            # ---------------------------------------
            # Only successful response
            # ---------------------------------------

            if response.status != 200:

                print(
                    f"⚠ Trend request returned "
                    f"HTTP {response.status}"
                )

                return

            data = response.json()

            # ---------------------------------------
            # Check response structure
            # ---------------------------------------

            if "creator_profile_trend_data" not in data:

                print(
                    "⚠ Type [4] response does not contain "
                    "'creator_profile_trend_data'"
                )

                return

            # ---------------------------------------
            # Save raw trend data
            # ---------------------------------------

            self.trend_data = data[
                "creator_profile_trend_data"
            ]

            print(
                "✓ Captured creator_profile_trend_data"
            )

        except Exception as ex:

            print(
                "⚠ Error while processing profile "
                f"API response: {ex}"
            )

    # ---------------------------------------------------------

    def get_trend_data(self):

        return self.trend_data

    # ---------------------------------------------------------

    def wait_until_ready(
        self,
        profile_page: Page
    ):

        print("Waiting for 'Creator details'...")

        profile_page.locator(
            "text=Creator details"
        ).wait_for(
            timeout=20000
        )

        print("✓ Creator details found")

        print("Waiting for Invite button...")

        profile_page.locator(
            "button:has-text('Invite')"
        ).wait_for(
            timeout=20000
        )

        print("✓ Invite button found")