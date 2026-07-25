from browser_manager import BrowserManager
from navigator import Navigator
from campaign import Campaign
from discovery_panel import DiscoveryPanel


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

browser = BrowserManager()
page = browser.start()

navigator = Navigator(page)
navigator.open_discover_creators(debug=True)

panel = DiscoveryPanel(page)
panel.apply_product_category(campaign)

input("Press ENTER to close...")

browser.stop()