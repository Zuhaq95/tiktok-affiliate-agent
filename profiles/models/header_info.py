from dataclasses import dataclass


@dataclass
class HeaderInfo:

    username: str = ""

    display_name: str = ""

    rating: float | None = None

    review_count: int = 0

    categories: str = ""

    followers: str = ""

    mcn: str = ""

    bio: str = ""

    email: str = ""

    website: str = ""