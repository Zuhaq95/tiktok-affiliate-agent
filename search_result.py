from dataclasses import dataclass
from playwright.sync_api import Locator

from creator import Creator


@dataclass
class SearchResult:
    """
    Represents one creator found in the TikTok search results.

    It contains:

    - creator:
        The parsed business data extracted from the search table.

    - click_target:
        The Playwright locator used to reopen the creator profile
        during deep analysis.

    This keeps browser automation separate from the Creator model.
    """

    creator: Creator

    click_target: Locator