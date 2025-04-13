from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers

class MaleoSOAPIEAssessmentGeneralParameters:
    class AssessmentIDs(BaseModel):
        assessment_ids:Optional[list[int]] = Field(None, description="Specific Assessment IDs")

    class ExpandableFields(StrEnum):
        DIAGNOSES = "diagnoses"

    class Expand(BaseModel):
        expand:list[MaleoSOAPIEAssessmentGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"

    class GetSingle(Expand, BaseGeneralParameters.GetSingle):
        identifier:MaleoSOAPIEAssessmentGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")

    class CreateOrUpdate(Expand, MaleoSOAPIEAssessmentGeneralTransfers.Base): pass