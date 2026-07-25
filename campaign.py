from dataclasses import dataclass


@dataclass
class Campaign:
    name: str

    keyword: str

   # product_category: str

    category: str

    subcategory: str

    content_language: str

    creator_gmv: str

    avg_commission: str

    content_type: str

    not_invited: bool