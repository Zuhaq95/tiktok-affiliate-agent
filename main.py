from browser_manager import BrowserManager
from navigator import Navigator
from discovery_panel import DiscoveryPanel
from creator_search import CreatorSearch
from creator_extractor import CreatorExtractor
from csv_exporter import CsvExporter
from campaign import Campaign
from config import DEBUG


def main():

    campaign = Campaign(
        name="UK Bedding",
        keyword="Mattress Topper",
        category="Textiles & Soft Furnishings",
        subcategory="Bedding",
        content_language="English",
        creator_gmv="£10K+",
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
        discovery_panel.apply_product_category(campaign)

        creator_search = CreatorSearch(page)
        creator_search.search(campaign.keyword)

        extractor = CreatorExtractor(page)
        creators = extractor.extract_visible_creators()

        print(f"\n✓ Extracted {len(creators)} creators\n")

        for creator in creators:
            print(creator)

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

        # Keep browser open only when debugging
        if DEBUG:
            input("\nPress ENTER to close...")

        browser.close()


if __name__ == "__main__":
    main()