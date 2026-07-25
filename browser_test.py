from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto("https://seller-uk.tiktok.com/")

    print("TikTok Seller Center opened!")

    page.wait_for_timeout(10000)

    browser.close()