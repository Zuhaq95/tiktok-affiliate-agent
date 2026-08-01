from dataclasses import dataclass


@dataclass
class Campaign:

    name: str

    keyword: str

    category: str

    subcategory: str

    content_language: str

    gmv: str

    avg_commission: str

    content_type: str

    not_invited: bool

    max_creators: int = 30