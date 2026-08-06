from dataclasses import dataclass


@dataclass
class CollaborationInfo:

    # -----------------------------------
    # Collaboration Metrics
    # -----------------------------------

    estimated_post_rate: str = ""
    estimated_post_rate_value: float = 0

    average_commission_rate: str = ""
    average_commission_rate_value: float = 0

    products: str = ""
    products_value: int = 0

    brand_collaborations: str = ""
    brand_collaborations_value: int = 0

    # -----------------------------------
    # Product Price
    # -----------------------------------

    product_price: str = ""

    minimum_product_price: float = 0

    maximum_product_price: float = 0