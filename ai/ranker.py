from creator import Creator


class Ranker:
    """
    Sorts creators by AI score.
    """

    @staticmethod
    def rank(creators: list[Creator]) -> list[Creator]:

        return sorted(
            creators,
            key=lambda creator: creator.ai_score,
            reverse=True
        )