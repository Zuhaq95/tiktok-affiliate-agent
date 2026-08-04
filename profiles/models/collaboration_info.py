from dataclasses import dataclass


@dataclass
class CollaborationInfo:

    estimated_post_rate: str = ""

    average_commission_rate: str = ""

    products: int = 0

    brand_collaborations: int = 0