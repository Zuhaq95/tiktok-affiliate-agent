from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="sessions/tiktok",
        headless=False
    )

    page = browser.new_page()

    page.goto("https://seller-uk.tiktok.com/")

    print("Please log into TikTok Seller Center.")

    input("After you have logged in completely, press ENTER here...")

    browser.close()