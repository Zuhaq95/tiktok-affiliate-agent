import re


class ParserUtils:

    @staticmethod
    def money_to_float(value: str) -> float:

        value = value.strip().replace("£", "")

        multiplier = 1

        if value.endswith("K"):

            multiplier = 1_000
            value = value[:-1]

        elif value.endswith("M"):

            multiplier = 1_000_000
            value = value[:-1]

        return float(value) * multiplier

    # ---------------------------------------------

    @staticmethod
    def percent_to_float(value: str) -> float:

        return float(
            value.replace("%", "")
        )

    # ---------------------------------------------

    @staticmethod
    def count_to_int(value: str) -> int:

        value = value.strip()

        multiplier = 1

        if value.endswith("K"):

            multiplier = 1_000
            value = value[:-1]

        elif value.endswith("M"):

            multiplier = 1_000_000
            value = value[:-1]

        return int(
            float(value) * multiplier
        )

    # ---------------------------------------------

    @staticmethod
    def extract_number(text: str):

        match = re.search(
            r"[\d.]+",
            text
        )

        if match:

            return float(match.group())

        return None