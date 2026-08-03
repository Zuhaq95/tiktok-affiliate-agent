from dataclasses import dataclass


@dataclass
class CreatorProfile:

    # --------------------------
    # Header Information
    # --------------------------

    username: str = ""
    display_name: str = ""

    rating: float = 0.0
    reviews: int = 0

    followers: str = ""

    categories: list[str] = None

    mcn: str = ""

    bio: str = ""

    # --------------------------
    # Sections
    # --------------------------

    sales = None
    collaboration = None
    video = None
    live = None
    followers_data = None
    trends = None
    similar_creators = None

    def __post_init__(self):

        if self.categories is None:
            self.categories = []