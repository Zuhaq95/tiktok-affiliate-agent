from creator_parser import CreatorParser
from ai.creator_normalizer import CreatorNormalizer
from profiles.creator_result import CreatorResult


class CreatorExtractor:

    def __init__(self, page):
        self.page = page
        self.parser = CreatorParser()

    def extract_visible_creators(self):

        print("\nExtracting visible creators...")

        tbodies = self.page.locator("tbody")

        tbody_count = tbodies.count()

        print(f"TBodies found: {tbody_count}")

        search_results = []

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

                    # Parse creator
                    creator = self.parser.parse(row)

                    # Populate normalized numeric values
                    CreatorNormalizer.normalize(creator)

                    # Keep both business data and browser element
                    search_results.append(
                        CreatorResult(
                            creator=creator,
                            row_locator=row
                        )
                    )

                except Exception as ex:
                    print(f"Row {row_index + 1} failed: {ex}")

            break

        print(
            f"\nSuccessfully extracted {len(search_results)} creators.\n"
        )

        return search_results