# pydbms/export/export_csv.py

import csv
from .export_base import Exporter


class CSVExporter(Exporter):
    """Exports a QueryResult as a CSV file.

    When include_query is True, the original SQL query is prepended
    as a comment row at the top of the file: ``# <SQL query>``.
    """

    def export(self, result, path: str, *, include_query: bool = False) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Embed the original SQL query as a comment row
            if include_query and hasattr(result, "query") and result.query:
                f.write(f"# {result.query}\n")

            writer.writerow(result.columns)
            writer.writerows(result.rows)
