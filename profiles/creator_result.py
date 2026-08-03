from dataclasses import dataclass

from creator import Creator


@dataclass
class CreatorResult:
    """
    Represents one creator discovered from the search results.

    It contains:
    - Quick creator information
    - The row locator used to reopen the profile
    """

    creator: Creator
    row_locator: object