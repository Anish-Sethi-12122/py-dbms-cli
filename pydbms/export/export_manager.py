# pydbms/export/export_manager.py

from .export_csv import CSVExporter
from .export_json import JSONExporter
import os
from datetime import datetime
from typing import Optional
from ..main.runtime import config
from ..main.pydbms_path import pydbms_path

class ExportManager:
    EXPORTERS = {
        "csv": CSVExporter,
        "json": JSONExporter,
    }

    @staticmethod
    def default_export_dir() -> str:
        return pydbms_path("exports")

    @staticmethod
    def default_export_filepath(fmt: str = "csv") -> str:
        user = config.get("mysql", {}).get("user", "unknown")

        filename = "-".join([
            "pydbms",
            "export",
            user,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ]) + f".{fmt}"

        return os.path.join(ExportManager.default_export_dir(), filename)

    @staticmethod
    def resolve_export_path(path: Optional[str], fmt: str) -> str:
        fmt = fmt.lower().lstrip(".")
        ext = f".{fmt}"

        # 1) no path => default export filepath
        if not path:
            return os.path.abspath(ExportManager.default_export_filepath(fmt))

        # 2) expand user (~) then return absolute path
        path = os.path.expanduser(path)
        abs_path = os.path.abspath(path)

        # 3) if it's an existing directory OR endswith path sep => treat as dir
        if os.path.isdir(abs_path) or path.endswith(("/", "\\")):
            filename = os.path.basename(ExportManager.default_export_filepath(fmt))
            return os.path.join(abs_path, filename)

        # 4) If user gave no extension
        if not abs_path.lower().endswith(ext):
            abs_path += ext

        return abs_path
    
    @staticmethod
    def normalize_export_dir(path: str) -> str:
        if not isinstance(path, str) or not path.strip():
            raise ValueError("export.path must be a non-empty directory path")

        raw = path.strip().strip('"').strip("'")
        raw = os.path.expanduser(raw)
        abs_path = os.path.abspath(raw)

        # If user gives a file-like path -> reject
        _, ext = os.path.splitext(abs_path)
        if ext:
            raise ValueError("Invalid export.path. It must be a DIRECTORY, not a file path "
                f"(got file extension '{ext}')."
            )

        # Create the directory if it doesn't exist
        try:
            os.makedirs(abs_path, exist_ok=True)
        except PermissionError:
            raise PermissionError(
                f"You do not have write permissions to create or access the directory: {abs_path}. "
                "Please choose another path or reset the config to default."
            )

        if not os.path.isdir(abs_path):
            raise ValueError("Invalid export.path. Path is not a directory.")

        return abs_path

    @staticmethod
    def export(
        fmt: str,
        result,
        path: Optional[str] = None,
        *,
        include_query: bool = False,
    ) -> str:
        """Export a QueryResult to a file in the specified format.

        Args:
            fmt: Export format key (e.g. 'csv', 'json').
            result: A QueryResult dataclass with .query, .columns, .rows.
            path: Optional user-specified output path. None = use default.
            include_query: If True, embed the original SQL query in the export.
                           Controlled by the --include-query flag (default: off).

        Returns:
            Absolute path to the written export file.

        Raises:
            ValueError: If the format is unsupported.
            PermissionError: If the export directory is not writable.
        """
        fmt = fmt.lower()
        supported = "{" + ", ".join(f'"{i}"' for i in sorted(ExportManager.EXPORTERS)) + "}"

        if fmt not in ExportManager.EXPORTERS:
            raise ValueError(
                f'Unsupported export format "{fmt}". '
                f"Supported formats: {supported}"
            )

        export_path = ExportManager.resolve_export_path(path, fmt)

        directory = os.path.dirname(export_path)
        if directory:
            try:
                os.makedirs(directory, exist_ok=True)
            except PermissionError:
                raise PermissionError(
                    f"You do not have write permissions to create or access the directory: {directory}. "
                    "Please choose another path or reset the config to default."
                )

        exporter = ExportManager.EXPORTERS[fmt]()
        exporter.export(result, export_path, include_query=include_query)

        return export_path
