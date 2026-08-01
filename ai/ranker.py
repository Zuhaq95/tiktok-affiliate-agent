from search_result import SearchResult


class Ranker:
    """
    Sorts search results by the creator's AI score.
    """

    @staticmethod
    def rank(search_results: list[SearchResult]) -> list[SearchResult]:

        return sorted(
            search_results,
            key=lambda result: result.creator.ai_score,
            reverse=True
        )