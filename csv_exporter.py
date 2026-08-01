from pathlib import Path
from datetime import datetime
import csv

from creator import Creator


class CsvExporter:

    def export(self, creators: list[Creator], keyword: str) -> Path:
        """
        Export ranked creators to a timestamped CSV file.

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
                "Rank",
                "AI Score",
                "Username",
                "Name",
                "Followers",
                "GMV",
                "Items Sold",
                "Avg Views",
                "Engagement",
                "Category",
                "Previously Invited",
                "AI Reasons"
            ])

            for rank, creator in enumerate(creators, start=1):

                writer.writerow([
                    rank,
                    creator.ai_score,
                    creator.username,
                    creator.name,
                    creator.followers,
                    creator.gmv,
                    creator.items_sold,
                    creator.avg_views,
                    creator.engagement,
                    creator.category,
                    creator.previously_invited,

                    # Join all AI explanations into one readable cell
                    " | ".join(creator.ai_reasons)
                ])

        print()
        print(f"✓ CSV exported to: {csv_file}")

        return csv_file