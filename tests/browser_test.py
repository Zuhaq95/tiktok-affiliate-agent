from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="sessions/tiktok",
        headless=False
    )

    page = browser.new_page()

    page.goto("https://affiliate.tiktok.com/?shop_region=GB")

    print("=" * 60)
    print("LOGIN TO YOUR UK TIKTOK AFFILIATE ACCOUNT")
    print("When you reach the Find Creators page, press ENTER here.")
    print("=" * 60)

    input()

    browser.close()