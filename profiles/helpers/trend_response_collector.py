import json

from playwright.sync_api import Page


class TrendResponseCollector:
    """
    Captures TikTok's creator profile trend API response.

    It listens for POST requests to /v1/list and only captures
    requests where profile_types contains exactly [4].
    """

    def __init__(self, page: Page):

        self.page = page

        self.trend_data = None

        self._handler = None

    # ---------------------------------------------------------

    def start(self):

        def handle_response(response):

            try:

                request = response.request

                # ---------------------------------------
                # Only POST requests
                # ---------------------------------------

                if request.method != "POST":
                    return

                # ---------------------------------------
                # Only TikTok list endpoint
                # ---------------------------------------

                if not request.url.endswith("/v1/list"):
                    return

                # ---------------------------------------
                # Read request payload
                # ---------------------------------------

                post_data = request.post_data

                if not post_data:
                    return

                payload = json.loads(post_data)

                # ---------------------------------------
                # We only want profile type [4]
                # ---------------------------------------

                profile_types = payload.get(
                    "profile_types"
                )

                if profile_types != [4]:
                    return

                print()
                print("✓ Found profile type 4 request")

                # ---------------------------------------
                # Read response
                # ---------------------------------------

                if response.status != 200:
                    print(
                        f"⚠ Trend request returned "
                        f"HTTP {response.status}"
                    )
                    return

                response_json = response.json()

                trend_data = response_json.get(
                    "creator_profile_trend_data"
                )

                if trend_data is None:
                    print(
                        "⚠ Type 4 response did not contain "
                        "'creator_profile_trend_data'"
                    )
                    return

                self.trend_data = trend_data

                print(
                    f"✓ Captured trend response "
                    f"({len(trend_data)} trend groups)"
                )

            except Exception as e:

                print(
                    f"⚠ Failed to capture trend response: {e}"
                )

        self._handler = handle_response

        self.page.context.on(
            "response",
            self._handler
        )

    # ---------------------------------------------------------

    def stop(self):

        if self._handler is not None:

            self.page.context.remove_listener(
                "response",
                self._handler
            )

            self._handler = None

    # ---------------------------------------------------------

    def get_data(self):

        return self.trend_data