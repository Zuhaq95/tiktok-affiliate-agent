from browser_manager import BrowserManager
from navigator import Navigator
from discovery_panel import DiscoveryPanel
from creator_search import CreatorSearch
from creator_extractor import CreatorExtractor
from csv_exporter import CsvExporter
from campaign import Campaign
from config import DEBUG
from ai.recommender import Recommender
from creator_collector import CreatorCollector

from ai.scorer import Scorer
from ai.ranker import Ranker


def main():

    campaign = Campaign(
        name="UK Bedding",
        keyword="Mattress Topper",
        category="Textiles & Soft Furnishings",
        subcategory="Bedding",
        content_language="English",
        gmv="£10K+",
        avg_commission="Less than 10%",
        content_type="Video",
        not_invited=True,
    )

    print(campaign)

    browser = BrowserManager()
    page = browser.start()

    try:

        navigator = Navigator(page)
        navigator.open_discover_creators()

        discovery_panel = DiscoveryPanel(page)
        discovery_panel.apply_filters(campaign)

        creator_search = CreatorSearch(page)
        creator_search.search(campaign.keyword)

        # extractor = CreatorExtractor(page)
        # creators = extractor.extract_visible_creators()

        collector = CreatorCollector(page)

        creators = collector.collect(
            campaign.max_creators
        )

        print(f"\n✓ Extracted {len(creators)} creators\n")

        # ----------------------------------------
        # AI Scoring
        # ----------------------------------------

        for creator in creators:
            Scorer.score(creator, campaign)
            Recommender.recommend(creator, campaign)

        # ----------------------------------------
        # AI Ranking
        # ----------------------------------------

        creators = Ranker.rank(creators)

        print("\n===== Ranked Creators =====\n")

        for index, creator in enumerate(creators, start=1):
            print(f"{index}. {creator.username}")
            print(f"   AI Score : {creator.ai_score}")

            for reason in creator.ai_reasons:
                print(f"   ✓ {reason}")

        print()
        exporter = CsvExporter()

        csv_file = exporter.export(
            creators,
            campaign.keyword
        )

        print(f"\n✓ CSV exported successfully:")
        print(csv_file)

    except Exception as ex:

        print("\nERROR:")
        print(type(ex).__name__)
        print(ex)
        raise

    finally:

        if DEBUG:
            input("\nPress ENTER to close...")

        browser.stop()


if __name__ == "__main__":
    main()