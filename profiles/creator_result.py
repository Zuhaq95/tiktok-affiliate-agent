from dataclasses import dataclass
from playwright.sync_api import Locator

from creator import Creator


@dataclass
class CreatorResult:
    """
    Represents one creator found in the search results.

    It contains:

    - The parsed Creator object (business data)
    - The Playwright locator that can reopen the profile

    This keeps browser automation separate from
    the business model.
    """

    creator: Creator

    click_target: Locator