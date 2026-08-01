from creator_extractor import CreatorExtractor


class CreatorCollector:

    def __init__(self, page):

        self.page = page
        self.extractor = CreatorExtractor(page)

    def collect(self, max_creators=30):

        print("\nCollecting creators...\n")

        creators = []
        seen = set()

        scroll_count = 0
        max_scrolls = 20
        no_new_scrolls = 0

        while len(creators) < max_creators and scroll_count < max_scrolls:

            print(f"\n===== Collection Cycle {scroll_count + 1} =====")

            visible_creators = self.extractor.extract_visible_creators()

            added = self.add_new_creators(
                visible_creators,
                creators,
                seen
            )

            self.log_progress(
                visible_creators,
                creators,
                added
            )

            if len(creators) >= max_creators:
                print("\n✓ Target creator count reached.")
                break

            if added == 0:
                no_new_scrolls += 1
            else:
                no_new_scrolls = 0

            if no_new_scrolls >= 3:
                print("\n✓ No new creators after 3 scrolls.")
                break

            self.scroll()

            scroll_count += 1

        print(f"\n✓ Final creator count: {len(creators)}")

        return creators[:max_creators]

    # ----------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------

    def add_new_creators(
        self,
        visible_creators,
        creators,
        seen
    ):

        added = 0

        for creator in visible_creators:

            if creator.username in seen:
                continue

            creators.append(creator)
            seen.add(creator.username)

            added += 1

        return added

    def scroll(self):

        print("\nScrolling...")

        container = self.page.locator("#scroll-container")

        before = container.evaluate("(e) => e.scrollTop")

        print(f"Scroll before : {before}")

        container.evaluate(
            "(e) => e.scrollBy(0,900)"
        )

        self.page.wait_for_timeout(1500)

        after = container.evaluate("(e) => e.scrollTop")

        print(f"Scroll after  : {after}")

    def log_progress(
        self,
        visible_creators,
        creators,
        added
    ):

        if visible_creators:

            print(
                f"First creator : {visible_creators[0].username}"
            )

            print(
                f"Last creator  : {visible_creators[-1].username}"
            )

        print(f"Visible creators : {len(visible_creators)}")
        print(f"New creators     : {added}")
        print(f"Total collected  : {len(creators)}")