# pydbms/export/export_json.py

from ..main.dependencies import json, datetime, decimal, base64
from .export_base import Exporter


class JSONExporter(Exporter):
    def export(self, result, path: str):
        def default(value):
            if isinstance(value, (datetime.date, datetime.datetime)):
                return value.isoformat()
            if isinstance(value, decimal.Decimal):
                return str(value)
            if isinstance(value, (bytes, bytearray)):
                return base64.b64encode(value).decode("ascii")
            return str(value)

        with open(path, "w", encoding="utf-8") as f:
            f.write("[\n")
            for i, row in enumerate(result.rows):
                if i:
                    f.write(",\n")
                json.dump(
                    dict(zip(result.columns, row)),
                    f,
                    ensure_ascii=False,
                    default=default
                )
            f.write("\n]")
