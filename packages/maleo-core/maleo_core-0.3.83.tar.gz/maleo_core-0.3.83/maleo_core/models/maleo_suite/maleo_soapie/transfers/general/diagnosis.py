from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoSOAPIEDiagnosisGeneralTransfers:
    class Base(BaseModel):
        assessment_id:int = Field(..., ge=1, description="Assessment's id")
        diagnosis:str = Field(..., description="Diagnosis")
        notes:Optional[str] = Field(None, description="Notes")