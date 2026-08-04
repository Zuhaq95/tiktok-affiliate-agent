from dataclasses import dataclass, field

from profiles.models.header_info import HeaderInfo
from profiles.models.sales_info import SalesInfo
from profiles.models.video_info import VideoInfo
from profiles.models.collaboration_info import CollaborationInfo
from profiles.models.trend_info import TrendInfo
from profiles.models.followers_info import FollowersInfo


@dataclass
class CreatorProfile:

    header: HeaderInfo = field(default_factory=HeaderInfo)

    sales: SalesInfo = field(default_factory=SalesInfo)

    videos: VideoInfo = field(default_factory=VideoInfo)

    audience: FollowersInfo = field(default_factory=FollowersInfo)

    trends: TrendInfo = field(default_factory=TrendInfo)