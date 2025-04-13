from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoSOAPIESOAPIEGeneralTransfers:
    class SOAPIEIDs(BaseModel):
        soapie_ids:Optional[list[int]] = Field(None, description="Specific SOAPIE IDs")