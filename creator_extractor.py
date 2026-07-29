from creator_parser import CreatorParser


class CreatorExtractor:

    def __init__(self, page):
        self.page = page
        self.parser = CreatorParser()

    def extract_visible_creators(self):

        print("\nExtracting visible creators...")

        tbodies = self.page.locator("tbody")

        tbody_count = tbodies.count()

        print(f"TBodies found: {tbody_count}")

        creators = []

        for tbody_index in range(tbody_count):

            tbody = tbodies.nth(tbody_index)

            rows = tbody.locator("tr")

            row_count = rows.count()

            print(f"TBody {tbody_index}: {row_count} rows")

            # Ignore empty tbodies
            if row_count == 0:
                continue

            # Ignore tiny tables (filters, summaries, etc.)
            if row_count < 3:
                continue

            print(f"\nUsing tbody {tbody_index}")

            for row_index in range(row_count):

                try:
                    row = rows.nth(row_index)

                    creator = self.parser.parse(row)

                    creators.append(creator)

                except Exception as ex:
                    print(f"Row {row_index + 1} failed: {ex}")

            break

        print(f"\nSuccessfully extracted {len(creators)} creators.\n")

        return creators