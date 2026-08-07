from dataclasses import dataclass, field
@dataclass
class FollowersInfo:

    gender_distribution: dict[str, float] = field(
        default_factory=dict
    )

    age_distribution: dict[str, float] = field(
        default_factory=dict
    )

    # TODO:
    # TikTok renders Top 5 locations on a canvas.
    # A future CanvasChartParser will populate this.
    top_locations: list[str] = field(
        default_factory=list
    )