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

            print(f"\n===== Scroll {scroll_count + 1} =====")

            visible_creators = self.extractor.extract_visible_creators()

            # Debug: show first and last creator currently visible
            if visible_creators:
                print(f"First creator : {visible_creators[0].username}")
                print(f"Last creator  : {visible_creators[-1].username}")

            added = 0

            for creator in visible_creators:

                if creator.username in seen:
                    continue

                creators.append(creator)
                seen.add(creator.username)
                added += 1

            print(f"Visible creators : {len(visible_creators)}")
            print(f"New creators     : {added}")
            print(f"Total collected  : {len(creators)}")

            # Stop if enough creators collected
            if len(creators) >= max_creators:
                print("\n✓ Target creator count reached.")
                break

            # Stop if nothing new appears after several scrolls
            if added == 0:
                no_new_scrolls += 1
            else:
                no_new_scrolls = 0

            if no_new_scrolls >= 3:
                print("\nNo new creators found after 3 consecutive scrolls.")
                break

            print("\nScrolling...")

            container = self.page.locator("#scroll-container")

            before = container.evaluate("(e) => e.scrollTop")
            print(f"Scroll before : {before}")

            container.evaluate("(e) => e.scrollBy(0, 900)")

            self.page.wait_for_timeout(1500)

            after = container.evaluate("(e) => e.scrollTop")
            print(f"Scroll after  : {after}")

            scroll_count += 1

        print(f"\n✓ Final creator count: {len(creators)}")

        return creators[:max_creators]