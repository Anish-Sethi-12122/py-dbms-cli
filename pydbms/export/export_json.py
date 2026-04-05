# pydbms/export/export_json.py

import json
from datetime import datetime, date
import decimal
import base64
from .export_base import Exporter


class JSONExporter(Exporter):
    """Exports a QueryResult as a JSON file.

    Output structure (include_query=True):
        { "query": "<SQL>", "rows": [ {col: val, ...}, ... ] }

    Output structure (include_query=False):
        [ {col: val, ...}, ... ]
    """

    def export(self, result, path: str, *, include_query: bool = False) -> None:
        def default(value):
            """Custom JSON serializer for non-standard Python types."""
            if isinstance(value, (date, datetime)):
                return value.isoformat()
            if isinstance(value, decimal.Decimal):
                return str(value)
            if isinstance(value, (bytes, bytearray)):
                return base64.b64encode(value).decode("ascii")
            return str(value)

        rows_data = [
            dict(zip(result.columns, row))
            for row in result.rows
        ]

        if include_query and hasattr(result, "query") and result.query:
            # Wrap in an object with the query and result rows
            output = {
                "query": result.query,
                "rows": rows_data,
            }
        else:
            # Flat array of row objects (legacy behavior)
            output = rows_data

        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2, default=default)
