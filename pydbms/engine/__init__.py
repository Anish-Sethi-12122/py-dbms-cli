# pydbms/engine/__init__.py

"""
Common engine module for pydbms.
Provides the abstract base class and standardized output helpers.
"""

from .engine_base import EngineBase, pydbms_error, pydbms_warning, pydbms_info

__all__ = ["EngineBase", "pydbms_error", "pydbms_warning", "pydbms_info"]
