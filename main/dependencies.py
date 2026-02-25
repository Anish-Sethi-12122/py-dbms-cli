# pydbms/pydbms/main/dependencies.py

import mysql.connector as mysql
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.table import Table
from rich.align import Align
from rich.rule import Rule
import pyfiglet
from importlib.metadata import version as pydbms_version
