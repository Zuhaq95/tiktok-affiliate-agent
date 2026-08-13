from pprint import pprint

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
from ai.scoring_context import ScoringContext
from ai.profile_scorer import ProfileScorer
from ai.content_relevance import ContentRelevance

from profiles.profile_opener import ProfileOpener
from profiles.profile_extractor import ProfileExtractor


# =========================================================
# Helper Methods
# =========================================================

def print_profile(profile):

    print()
    print("=" * 60)
    print("HEADER DATA")
    print("=" * 60)

    print(
        "Username     :",
        profile.header.username
    )

    print(
        "Display Name :",
        profile.header.display_name
    )

    print(
        "Rating       :",
        profile.header.rating
    )

    print(
        "Reviews      :",
        profile.header.review_count
    )

    print(
        "Categories   :",
        profile.header.categories
    )

    print(
        "Followers    :",
        profile.header.followers
    )

    print(
        "MCN          :",
        profile.header.mcn
    )

    print(
        "Email        :",
        profile.header.email
    )

    print(
        "Website      :",
        profile.header.website
    )

    print()

    print("Bio:")
    print(
        profile.header.bio
    )

    print()
    print("=" * 60)
    print("SALES DATA")
    print("=" * 60)

    print(
        "Report Period        :",
        profile.sales.report_period
    )

    print(
        "GMV                  :",
        profile.sales.total_gmv
    )

    print(
        "Items Sold           :",
        profile.sales.items_sold
    )

    print(
        "GPM                  :",
        profile.sales.gpm
    )

    print(
        "GMV / Customer       :",
        profile.sales.gmv_per_customer
    )

    print()
    print("Sales Channels")
    print(
        profile.sales.sales_channel_distribution
    )

    print()
    print("Category Distribution")
    print(
        profile.sales.category_distribution
    )


# =========================================================
# Main
# =========================================================

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

        # =================================================
        # Navigation
        # =================================================

        navigator = Navigator(
            page
        )

        navigator.open_discover_creators()

        # =================================================
        # Apply Filters
        # =================================================

        discovery_panel = DiscoveryPanel(
            page
        )

        discovery_panel.apply_filters(
            campaign
        )

        # =================================================
        # Search
        # =================================================

        creator_search = CreatorSearch(
            page
        )

        creator_search.search(
            campaign.keyword
        )

        # =================================================
        # Collect Creators
        # =================================================

        collector = CreatorCollector(
            page
        )

        search_results = collector.collect(
            campaign.max_creators
        )

        print(
            f"\n✓ Extracted "
            f"{len(search_results)} creators\n"
        )

        # =================================================
        # Basic Scoring
        # =================================================

        for result in search_results:

            Scorer.score(
                result.creator,
                campaign
            )

            Recommender.recommend(
                result.creator,
                campaign
            )

        # =================================================
        # Basic Ranking
        # =================================================

        search_results = Ranker.rank(
            search_results
        )

        # =================================================
        # Console Output
        # =================================================

        print(
            "\n===== Ranked Creators =====\n"
        )

        for index, result in enumerate(
            search_results,
            start=1
        ):

            creator = result.creator

            print(
                f"{index}. "
                f"{creator.username}"
            )

            print(
                f"   AI Score : "
                f"{creator.ai_score}"
            )

            for reason in creator.ai_reasons:

                print(
                    f"   ✓ {reason}"
                )

        # =================================================
        # Export CSV
        # =================================================

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

        print(
            csv_file
        )

        # =================================================
        # TESTING ONLY
        #
        # Open first creator profile
        # =================================================

        opener = ProfileOpener(
            page
        )

        print(
            "\nOpening first creator...\n"
        )

        result = search_results[0]

        profile_page = opener.open(
            result
        )

        # =================================================
        # Extract Detailed Creator Profile
        # =================================================

        extractor = ProfileExtractor(
            profile_page,
            trend_data=opener.get_trend_data()
        )

        profile = extractor.extract()

        # =================================================
        # Attach Profile To Creator
        # =================================================

        result.creator.profile = profile

        print()
        print("=" * 60)
        print("ATTACHED CREATOR PROFILE")
        print("=" * 60)

        print(
            "Creator:",
            result.creator.username
        )

        print(
            "Profile username:",
            result.creator.profile.header.username
        )

        print(
            "Profile GMV:",
            result.creator.profile.sales.total_gmv
        )

        print(
            "Profile followers:",
            result.creator.profile.header.followers
        )

        print(
            "Report period:",
            result.creator.profile.sales.report_period
        )

        print(
            "Trend points:",
            len(
                result.creator.profile.trends.gmv_trend or []
            )
        )

        print(
            "Example videos:",
            len(
                result.creator.profile.example_videos
            )
        )

        print(
            "Product videos:",
            len(
                result.creator.profile.product_videos
            )
        )

        print(
            "\n✓ Detailed profile attached to creator."
        )

        # =================================================
        # Build Profile Scoring Context
        # =================================================

        context = ScoringContext.build(
            result.creator,
            campaign
        )

        # =================================================
        # Deterministic Profile Score
        # =================================================

        profile_score = ProfileScorer.score(
            context
        )

        print(
            f"\nProfile score: "
            f"{profile_score}"
        )

        # =================================================
        # PROFILE SCORING SIGNALS
        # =================================================

        signals = (
            context.profile_signals
        )

        print()
        print("=" * 60)
        print("PROFILE SCORING SIGNALS")
        print("=" * 60)

        # -----------------------------------------
        # Video content
        # -----------------------------------------

        print(
            "Example videos:",
            signals.example_video_count
        )

        print(
            "Product videos:",
            signals.product_video_count
        )

        print(
            "Product videos with products:",
            signals.product_video_count_with_products
        )

        print(
            "Video captions:",
            signals.video_captions
        )

        print(
            "Product video captions:",
            signals.product_video_captions
        )

        print(
            "Product video avg views:",
            signals.product_video_average_views
        )

        print(
            "Product video avg likes:",
            signals.product_video_average_likes
        )

        # -----------------------------------------
        # Activity
        # -----------------------------------------

        print(
            "Latest video age (days):",
            signals.latest_video_age_days
        )

        print(
            "Videos in last 30 days:",
            signals.videos_last_30_days
        )

        # -----------------------------------------
        # View consistency
        # -----------------------------------------

        print(
            "Video view consistency:",
            signals.video_view_consistency
        )

        print(
            "Product video view consistency:",
            signals.product_video_view_consistency
        )

        # -----------------------------------------
        # Engagement
        # -----------------------------------------

        print(
            "Average video like rate:",
            signals.average_video_like_rate
        )

        print(
            "Product video like rate:",
            signals.product_video_like_rate
        )

        # -----------------------------------------
        # Posting consistency
        # -----------------------------------------

        print(
            "Average days between videos:",
            signals.average_days_between_videos
        )

        print(
            "Posting consistency:",
            signals.posting_consistency
        )

        # =================================================
        # HISTORICAL TREND SIGNALS
        # =================================================

        print()
        print("=" * 60)
        print("HISTORICAL TREND SIGNALS")
        print("=" * 60)

        print(
            "Average GMV:",
            signals.average_gmv
        )

        print(
            "Median GMV:",
            signals.median_gmv
        )

        print(
            "GMV consistency:",
            signals.gmv_consistency
        )

        print(
            "GMV periods above £1K:",
            signals.gmv_periods_above_1000
        )

        print(
            "GMV periods above £2K:",
            signals.gmv_periods_above_2000
        )

        print(
            "Average units sold:",
            signals.average_units_sold
        )

        print(
            "Median units sold:",
            signals.median_units_sold
        )

        print(
            "Average trend video views:",
            signals.average_trend_video_views
        )

        print(
            "Median trend video views:",
            signals.median_trend_video_views
        )

        print(
            "Follower growth:",
            signals.follower_growth
        )

        print(
            "GMV momentum:",
            signals.gmv_momentum
        )

        print(
            "Sales momentum:",
            signals.sales_momentum
        )

        print(
            "Video views momentum:",
            signals.video_views_momentum
        )

        # =================================================
        # CAMPAIGN FIT
        # =================================================

        print()
        print("=" * 60)
        print("CAMPAIGN FIT SIGNALS")
        print("=" * 60)

        print(
            "Campaign category GMV %:",
            signals.campaign_category_gmv_percentage
        )

        print(
            "Campaign content type sales %:",
            signals.campaign_content_type_sales_percentage
        )

        # =================================================
        # COLLABORATION
        # =================================================

        print()
        print("=" * 60)
        print("COLLABORATION SIGNALS")
        print("=" * 60)

        print(
            "Brand collaborations:",
            signals.brand_collaborations
        )

        print(
            "Products:",
            signals.products
        )

        print(
            "Average commission:",
            signals.average_commission_rate
        )

        # =================================================
        # GEMINI CONTENT RELEVANCE
        # =================================================

        print()
        print("=" * 60)
        print("GEMINI CONTENT RELEVANCE")
        print("=" * 60)

        print(
            "Analyzing creator content with Gemini..."
        )

        content_relevance = ContentRelevance()

        relevance_result = (
            content_relevance.analyze(
                context
            )
        )

        print()
        print(
            "Gemini relevance result:"
        )

        pprint(
            relevance_result
        )

        # =================================================
        # Individual Gemini Signals
        # =================================================

        print()

        print(
            "Content relevance score:",
            relevance_result.get(
                "relevance_score"
            )
        )

        print(
            "Campaign match:",
            relevance_result.get(
                "campaign_match"
            )
        )

        print(
            "Confidence:",
            relevance_result.get(
                "confidence"
            )
        )

        print(
            "Matched topics:",
            relevance_result.get(
                "matched_topics"
            )
        )

        print(
            "Missing topics:",
            relevance_result.get(
                "missing_topics"
            )
        )

        print()

        print(
            "Reasons:"
        )

        for reason in (
            relevance_result.get(
                "reasons",
                []
            )
        ):

            print(
                f"  ✓ {reason}"
            )

        # =================================================
        # IMPORTANT
        #
        # We are NOT combining the Gemini score with
        # ProfileScore yet.
        # =================================================

        print()
        print(
            "Profile score:",
            profile_score
        )

        print(
            "Gemini content score:",
            relevance_result.get(
                "relevance_score"
            )
        )

        print(
            "Final score: NOT CALCULATED YET"
        )

        # =================================================
        # AI CONTENT RELEVANCE INPUT
        # =================================================

        print()
        print("=" * 60)
        print("AI CONTENT RELEVANCE PROMPT")
        print("=" * 60)

        prompt = (
            ContentRelevance.build_prompt(
                context
            )
        )

        print(
            prompt
        )

        # =================================================
        # TEST VIDEO BUTTON
        # =================================================

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
                print(
                    "Video URL:"
                )

                print(
                    video_page.url
                )

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

                print(
                    ex
                )

        # =================================================
        # Keep Browser Open For Debugging
        # =================================================

        profile_page.pause()

    except Exception as ex:

        print(
            "\nERROR:"
        )

        print(
            type(ex).__name__
        )

        print(
            ex
        )

        raise

    finally:

        if DEBUG:

            input(
                "\nPress ENTER to close..."
            )

        browser.stop()


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":
    main()