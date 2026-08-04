from dataclasses import dataclass, field

from profiles.models.header_info import HeaderInfo
from profiles.models.sales_info import SalesInfo
from profiles.models.collaboration_info import CollaborationInfo
from profiles.models.video_info import VideoInfo
from profiles.models.followers_info import FollowersInfo
from profiles.models.trend_info import TrendInfo


@dataclass
class CreatorProfile:

    header: HeaderInfo = field(default_factory=HeaderInfo)

    sales: SalesInfo = field(default_factory=SalesInfo)

    collaboration: CollaborationInfo = field(default_factory=CollaborationInfo)

    videos: VideoInfo = field(default_factory=VideoInfo)

    followers: FollowersInfo = field(default_factory=FollowersInfo)

    trends: TrendInfo = field(default_factory=TrendInfo)