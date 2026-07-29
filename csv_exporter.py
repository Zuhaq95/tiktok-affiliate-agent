from pathlib import Path
from datetime import datetime
import csv

from creator import Creator


class CsvExporter:

    def export(self, creators: list[Creator], keyword: str) -> Path:
        """
        Export creators to a timestamped CSV file.

        Returns:
            Path to the generated CSV.
        """

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        safe_keyword = (
            keyword.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        csv_file = output_dir / f"{safe_keyword}_{timestamp}.csv"

        with open(csv_file, "w", newline="", encoding="utf-8-sig") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Username",
                "Name",
                "Followers",
                "Category",
                "GMV",
                "Items Sold",
                "Avg Views",
                "Engagement",
                "Previously Invited"
            ])

            for creator in creators:

                writer.writerow([
                    creator.username,
                    creator.name,
                    creator.followers,
                    creator.category,
                    creator.gmv,
                    creator.items_sold,
                    creator.avg_views,
                    creator.engagement,
                    creator.previously_invited
                ])

        print()
        print(f"✓ CSV exported to: {csv_file}")

        return csv_file