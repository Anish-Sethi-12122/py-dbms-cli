# pydbms/pydbms/main/dependencies.py

import mysql.connector as mysql
from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.table import Table
from rich.align import Align
from rich.rule import Rule
from dataclasses import dataclass
from typing import List, Any, Optional, Protocol
from crypto_functions import hash_argon2
import shlex
import sqlparse
import pwinput
import time
import sys
import pyfiglet
import re
import os
import json
import copy
from datetime import datetime
import csv
import decimal
import base64
from importlib.metadata import version as pydbms_version
