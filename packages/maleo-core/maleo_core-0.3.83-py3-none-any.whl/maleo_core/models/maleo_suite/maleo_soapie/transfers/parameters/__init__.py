# This file serves all MaleoSOAPIE's Parameters

from __future__ import annotations
from .general import MaleoAcccesGeneralParameters
from .service import MaleoSOAPIEServiceParameters
from .client import MaleoSOAPIEClientParameters

class MaleoSOAPIEParameters:
    General = MaleoAcccesGeneralParameters
    Service = MaleoSOAPIEServiceParameters
    Client = MaleoSOAPIEClientParameters

__all__ = [
    "MaleoSOAPIEParameters",
    "MaleoAcccesGeneralParameters",
    "MaleoSOAPIEServiceParameters",
    "MaleoSOAPIEClientParameters"
]