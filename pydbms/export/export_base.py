# pydbms/export/export_base.py

from abc import ABC, abstractmethod


class Exporter(ABC):
    """Base class for all export format implementations.

    Subclasses must implement export() to write a QueryResult to disk.
    """

    @abstractmethod
    def export(self, result, path: str, *, include_query: bool = False) -> None:
        """Write a QueryResult to the given file path.

        Args:
            result: A QueryResult dataclass with .query, .columns, and .rows.
            path: Absolute file path to write the export to.
            include_query: If True, embed the original SQL query in the export.
                           Default: off — user opts in with --include-query.
        """
        raise NotImplementedError