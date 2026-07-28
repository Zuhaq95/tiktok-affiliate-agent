from csv import reader
from re import search

from browser_manager import BrowserManager
import campaign
from navigator import Navigator
from campaign import Campaign
from discovery_panel import DiscoveryPanel
from creator_search import CreatorSearch
from creator_extractor import CreatorExtractor


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
        not_invited=True
    )

    print(campaign)
# open browser and start a new page
    browser = BrowserManager()
    page = browser.start()

    try:
    # open the affiliate portal and navigate to the Discover Creators page
        navigator = Navigator(page)
        navigator.open_discover_creators()
    # apply the product category filter, search for creators, and read the results
        panel = DiscoveryPanel(page)
        panel.apply_product_category(campaign)
    # search for creators using the specified keyword from the campaign in Main.py
        search = CreatorSearch(page)
        search.search(campaign.keyword)
    # read the creators  on the page and print the results
        extractor = CreatorExtractor(page)
        creators = extractor.extract_visible_creators()
        print(creators)

        input("Press ENTER to close...")

    finally:
        browser.stop()


if __name__ == "__main__":
    main()