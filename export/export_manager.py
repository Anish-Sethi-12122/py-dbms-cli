# pydbms/export/export_manager.py

from .export_csv import CSVExporter
from ..dependencies import os

class export_manager:
    EXPORTERS = {
        "csv": CSVExporter
    }

    @staticmethod
    def export(fmt: str, result, path: str) -> str | None:
        fmt = fmt.lower()
        if fmt not in export_manager.EXPORTERS:
            return None

        exporter = export_manager.EXPORTERS[fmt]()
        exporter.export(result, path)
        
        return os.path.abspath(path)
