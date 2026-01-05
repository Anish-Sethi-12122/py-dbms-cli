# pydbms/export/export_csv.py

from ..dependencies import csv
from .export_base import Exporter

class CSVExporter(Exporter):
    def export(self, result, path: str):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(result.columns)
            writer.writerows(result.rows)
