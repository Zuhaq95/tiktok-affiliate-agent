from creator_extractor import CreatorExtractor


class CreatorCollector:

    def __init__(self, page):

        self.page = page
        self.extractor = CreatorExtractor(page)

    def collect(self, max_creators=30):

        print("\nCollecting creators...\n")

        creators = self.extractor.extract_visible_creators()

        print(f"Collected {len(creators)} creators.")

        return creators