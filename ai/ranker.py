from profiles.creator_result import CreatorResult


class Ranker:
    """
    Sorts creators by AI score.
    """

    @staticmethod
    def rank(results: list[CreatorResult]) -> list[CreatorResult]:

        return sorted(
            results,
            key=lambda result: result.creator.ai_score,
            reverse=True
        )