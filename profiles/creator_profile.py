from dataclasses import dataclass, field

from profiles.models.header_info import HeaderInfo
from profiles.models.sales_info import SalesInfo
from profiles.models.collaboration_info import CollaborationInfo
from profiles.models.video_info import VideoInfo
from profiles.models.live_info import LiveInfo
from profiles.models.followers_info import FollowersInfo
from profiles.models.trend_info import TrendInfo
from profiles.models.video_card_info import VideoCardInfo


@dataclass
class CreatorProfile:

    header: HeaderInfo = field(
        default_factory=HeaderInfo
    )

    sales: SalesInfo = field(
        default_factory=SalesInfo
    )

    collaboration: CollaborationInfo = field(
        default_factory=CollaborationInfo
    )

    videos: VideoInfo = field(
        default_factory=VideoInfo
    )

    live: LiveInfo = field(
        default_factory=LiveInfo
    )

    followers: FollowersInfo = field(
        default_factory=FollowersInfo
    )

    trends: TrendInfo = field(
        default_factory=TrendInfo
    )

    example_videos: list[VideoCardInfo] = field(
        default_factory=list
    )

    product_videos: list[VideoCardInfo] = field(
        default_factory=list
    )