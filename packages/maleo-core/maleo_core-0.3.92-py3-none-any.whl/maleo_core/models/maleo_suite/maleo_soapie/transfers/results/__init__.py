# This file serves all MaleoSOAPIE's Results

from __future__ import annotations
from .client import MaleoSOAPIEClientResults
from .service import MaleoSOAPIEServiceResults
from .query import MaleoSOAPIEQueryResults
from .general import MaleoSOAPIEGeneralResults

class MaleoSOAPIEResults:
    Client = MaleoSOAPIEClientResults
    Service = MaleoSOAPIEServiceResults
    Query = MaleoSOAPIEQueryResults
    General = MaleoSOAPIEGeneralResults

__all__ = [
    "MaleoSOAPIEResults",
    "MaleoSOAPIEClientResults",
    "MaleoSOAPIEServiceResults",
    "MaleoSOAPIEQueryResults",
    "MaleoSOAPIEGeneralResults"
]