from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.vital_sign import MaleoSOAPIEVitalSignGeneralTransfers

class MaleoSOAPIEObjectiveGeneralTransfers:
    class Base(BaseModel):
        soapie_id:int = Field(..., ge=1, description="SOAPIE's id")
        overall:str = Field(..., description="Overall objective")
        vital_sign:Optional[MaleoSOAPIEVitalSignGeneralTransfers.Base] = Field(None, description="Vital Sign")
        other_information:Optional[str] = Field(None, description="Other information")