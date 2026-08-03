from browser_manager import BrowserManager

browser = BrowserManager()
page = browser.start()

input("Navigate manually to the Creator page, perform the search, then press ENTER...")

html = page.content()

with open("page_dump.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Page dumped successfully.")

input("Press ENTER to close...")

browser.stop()