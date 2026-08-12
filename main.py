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
from profiles.profile_extractor import ProfileExtractor


# ---------------------------------------------------------
# Helper Methods
# ---------------------------------------------------------

def print_profile(profile):

    print()
    print("=" * 60)
    print("HEADER DATA")
    print("=" * 60)

    print("Username     :", profile.header.username)
    print("Display Name :", profile.header.display_name)
    print("Rating       :", profile.header.rating)
    print("Reviews      :", profile.header.review_count)
    print("Categories   :", profile.header.categories)
    print("Followers    :", profile.header.followers)
    print("MCN          :", profile.header.mcn)
    print("Email        :", profile.header.email)
    print("Website      :", profile.header.website)

    print()
    print("Bio:")
    print(profile.header.bio)

    print()
    print("=" * 60)
    print("SALES DATA")
    print("=" * 60)

    print("GMV                  :", profile.sales.total_gmv)
    print("Items Sold           :", profile.sales.items_sold)
    print("GPM                  :", profile.sales.gpm)
    print("GMV / Customer       :", profile.sales.gmv_per_customer)

    print()
    print("Sales Channels")
    print(profile.sales.sales_channel_distribution)

    print()
    print("Category Distribution")
    print(profile.sales.category_distribution)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    campaign = Campaign(
        name="UK Bedding",
        keyword="Box Stitched Duvet",
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

        print(
            f"\n✓ Extracted {len(search_results)} creators\n"
        )

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

        search_results = Ranker.rank(
            search_results
        )

        # ----------------------------------------
        # Console Output
        # ----------------------------------------

        print("\n===== Ranked Creators =====\n")

        for index, result in enumerate(
            search_results,
            start=1
        ):

            creator = result.creator

            print(
                f"{index}. {creator.username}"
            )

            print(
                f"   AI Score : {creator.ai_score}"
            )

            for reason in creator.ai_reasons:

                print(
                    f"   ✓ {reason}"
                )

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

        print(
            "\n✓ CSV exported successfully:"
        )

        print(csv_file)

        # ----------------------------------------
        # TESTING ONLY
        # ----------------------------------------

        opener = ProfileOpener(page)

        print(
            "\nOpening first creator...\n"
        )

        result = search_results[0]

        profile_page = opener.open(
            result
        )

        # ----------------------------------------
        # Extract Detailed Creator Profile
        # ----------------------------------------

        extractor = ProfileExtractor(
            profile_page,
            trend_data=opener.get_trend_data()
        )

        profile = extractor.extract()

        # ----------------------------------------
        # Attach Profile To Creator
        # ----------------------------------------

        result.creator.profile = profile

        print()
        print("=" * 60)
        print("ATTACHED CREATOR PROFILE")
        print("=" * 60)

        print("Creator:", result.creator.username)

        print("Profile username:", result.creator.profile.header.username)

        print("Profile GMV:", result.creator.profile.sales.total_gmv)

        print("Profile followers:", result.creator.profile.header.followers)

        print("Trend points:", len(
            result.creator.profile.trends.gmv_trend or []
        ))

        print("Example videos:", len(
            result.creator.profile.example_videos
        ))

        print("Product videos:", len(
            result.creator.profile.product_videos
        ))

        print(
            "\n✓ Detailed profile attached to creator."
        )

        # ----------------------------------------
        # TEST VIDEO "View video on TikTok"
        # ----------------------------------------

        print()
        print("=" * 60)
        print("TESTING VIDEO BUTTON")
        print("=" * 60)

        example_section = profile_page.locator(
            "div.bg-white"
        ).nth(9)

        button = example_section.get_by_text(
            "View video on TikTok",
            exact=True
        ).first

        print(
            "Button count:",
            button.count()
        )

        if button.count() == 0:

            print(
                "❌ View video on TikTok button not found"
            )

        else:

            print(
                "✓ View video on TikTok button found"
            )

            try:

                with profile_page.expect_popup(
                    timeout=5000
                ) as popup_info:

                    button.click()

                video_page = popup_info.value

                print(
                    "✓ Popup opened"
                )

                print()
                print("Video URL:")
                print(video_page.url)

                video_page.close()

                print(
                    "✓ Popup closed"
                )

            except Exception as ex:

                print()
                print(
                    "❌ No popup opened"
                )

                print(
                    type(ex).__name__
                )

                print(ex)

        # ----------------------------------------
        # Keep Browser Open For Debugging
        # ----------------------------------------

        profile_page.pause()

    except Exception as ex:

        print(
            "\nERROR:"
        )

        print(
            type(ex).__name__
        )

        print(ex)

        raise

    finally:

        if DEBUG:

            input(
                "\nPress ENTER to close..."
            )

        browser.stop()


if __name__ == "__main__":
    main()