from creator_extractor import CreatorExtractor


class CreatorCollector:

    def __init__(self, page):

        self.page = page
        self.extractor = CreatorExtractor(page)

    def collect(self, max_creators=30):

        print("\nCollecting creators...\n")

        search_results = []
        seen = set()

        scroll_count = 0
        max_scrolls = 20
        no_new_scrolls = 0

        while len(search_results) < max_creators and scroll_count < max_scrolls:

            print(f"\n===== Collection Cycle {scroll_count + 1} =====")

            visible_results = self.extractor.extract_visible_creators()

            added = self.add_new_creators(
                visible_results,
                search_results,
                seen
            )

            self.log_progress(
                visible_results,
                search_results,
                added
            )

            if len(search_results) >= max_creators:
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

        print(f"\n✓ Final creator count: {len(search_results)}")

        return search_results[:max_creators]

    # ----------------------------------------------------
    # Helper Methods
    # ----------------------------------------------------

    def add_new_creators(
        self,
        visible_results,
        search_results,
        seen
    ):

        added = 0

        for result in visible_results:

            creator = result.creator

            if creator.username in seen:
                continue

            search_results.append(result)

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
        visible_results,
        search_results,
        added
    ):

        if visible_results:

            print(
                f"First creator : {visible_results[0].creator.username}"
            )

            print(
                f"Last creator  : {visible_results[-1].creator.username}"
            )

        print(f"Visible creators : {len(visible_results)}")
        print(f"New creators     : {added}")
        print(f"Total collected  : {len(search_results)}")