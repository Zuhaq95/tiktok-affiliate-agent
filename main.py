from browser_manager import BrowserManager
from navigator import Navigator
from discovery_panel import DiscoveryPanel
from creator_search import CreatorSearch
from creator_collector import CreatorCollector
from csv_exporter import CsvExporter

from campaign import Campaign
from config import DEBUG

from ai.scorer import Scorer
from ai.recommender import Recommender
from ai.ranker import Ranker

from profiles.profile_opener import ProfileOpener


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

        # ----------------------------------------
        # Navigation
        # ----------------------------------------

        navigator = Navigator(page)
        navigator.open_discover_creators()

        # ----------------------------------------
        # Apply Filters
        # ----------------------------------------

        discovery_panel = DiscoveryPanel(page)
        discovery_panel.apply_filters(campaign)

        # ----------------------------------------
        # Search
        # ----------------------------------------

        creator_search = CreatorSearch(page)
        creator_search.search(campaign.keyword)

        # ----------------------------------------
        # Collect Creators
        # ----------------------------------------

        collector = CreatorCollector(page)

        search_results = collector.collect(
            campaign.max_creators
        )

        print(f"\n✓ Extracted {len(search_results)} creators\n")

        # ----------------------------------------
        # AI Scoring
        # ----------------------------------------

        for result in search_results:

            Scorer.score(
                result.creator,
                campaign
            )

            Recommender.recommend(
                result.creator,
                campaign
            )

        # ----------------------------------------
        # AI Ranking
        # ----------------------------------------

        search_results = Ranker.rank(search_results)

        # ----------------------------------------
        # Console Output
        # ----------------------------------------

        print("\n===== Ranked Creators =====\n")

        for index, result in enumerate(search_results, start=1):

            creator = result.creator

            print(f"{index}. {creator.username}")
            print(f"   AI Score : {creator.ai_score}")

            for reason in creator.ai_reasons:
                print(f"   ✓ {reason}")

        # ----------------------------------------
        # Export CSV
        # ----------------------------------------

        creators = [
            result.creator
            for result in search_results
        ]

        exporter = CsvExporter()

        csv_file = exporter.export(
            creators,
            campaign.keyword
        )

        print("\n✓ CSV exported successfully:")
        print(csv_file)

        # ----------------------------------------
        # Open First Creator (Testing)
        # ----------------------------------------

        opener = ProfileOpener(page)

        print("\nOpening first creator...\n")

        profile_page = opener.open(
            search_results[0]
        )

        profile_page.pause()

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