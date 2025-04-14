"""
JSONPath-NZ
===========

A Python library for bidirectional conversion between JSON objects and JSONPath expressions.
Handles complex filter conditions, nested arrays, and maintains data structure integrity.

Author: Yakub Mohammad | Rishaad 
Version: 0.1.4
Company: AR USA LLC
License: MIT
Copyright (c) 2024 AR USA LLC support@arusatech.com
"""

from .parse_dict import parse_dict
from .parse_jsonpath import parse_jsonpath
from .merge_json import merge_json
from .log import log
from .jprint import jprint

__version__ = "0.1.4"
__author__ = "Yakub Mohammad | Rishaad"
__license__ = "MIT"

__all__ = [
    "parse_dict",
    "parse_jsonpath",
    "merge_json",
    "log",
    "jprint"
]
