import re


class Normalizer:
    """
    Converts TikTok formatted strings into numeric values.
    """

    @staticmethod
    def followers(value: str) -> int:
        return int(Normalizer._parse_suffix_number(value))

    @staticmethod
    def gmv(value: str) -> float:
        value = value.replace("£", "").replace(",", "")
        return Normalizer._parse_suffix_number(value)

    @staticmethod
    def items_sold(value: str) -> float:
        return Normalizer._parse_suffix_number(value)

    @staticmethod
    def avg_views(value: str) -> float:
        return Normalizer._parse_suffix_number(value)

    @staticmethod
    def engagement(value: str) -> float:
        return float(value.replace("%", "").strip())

    @staticmethod
    def _parse_suffix_number(value: str) -> float:

        value = value.strip().upper()

        match = re.match(r"([\d.]+)([KMB]?)", value)

        if not match:
            return 0

        number = float(match.group(1))
        suffix = match.group(2)

        multipliers = {
            "": 1,
            "K": 1_000,
            "M": 1_000_000,
            "B": 1_000_000_000
        }

        return number * multipliers.get(suffix, 1)