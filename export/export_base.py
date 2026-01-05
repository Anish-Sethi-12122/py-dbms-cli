# pydbms/export/export_base.py

class Exporter:
    def export(self, result, path: str):
        raise NotImplementedError
