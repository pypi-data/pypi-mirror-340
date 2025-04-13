from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.diagnosis import MaleoSOAPIEDiagnosisGeneralTransfers

class MaleoSOAPIEAssessmentGeneralTransfers:
    class Base(BaseModel):
        soapie_id:int = Field(..., ge=1, description="SOAPIE's id")
        overall:str = Field(..., description="Overall assessment")
        diagnoses:list[MaleoSOAPIEDiagnosisGeneralTransfers.Base] = Field([], description="Diagnoses")
        other_information:Optional[str] = Field(None, description="Other information")