# pydbms/export/export_manager.py

from .export_csv import CSVExporter
from .export_json import JSONExporter
from ..main.dependencies import os, datetime
from ..main.profile import PROFILE

class ExportManager:
    EXPORTERS = {
        "csv": CSVExporter,
        "json": JSONExporter,
    }

    @staticmethod
    def default_export_path(fmt: str) -> str:
        user = getattr(PROFILE, "user", "root")
        filename = "-".join([
            "pydbms",
            "export",
            user,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ]) + f".{fmt}"
        
        return os.path.join("exports", filename)

    @staticmethod
    def export(fmt: str, result, path: str | None = None) -> str:
        fmt = fmt.lower()
        supported = "{" + ", ".join(f'"{i}"' for i in sorted(ExportManager.EXPORTERS)) + "}"

        if fmt not in ExportManager.EXPORTERS:
            raise ValueError(
                f'Unsupported export format "{fmt}". '
                f"Supported formats: {supported}"
            )

        if not path:
            path = ExportManager.default_export_path(fmt)

        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        exporter = ExportManager.EXPORTERS[fmt]()
        exporter.export(result, path)

        return os.path.abspath(path)
