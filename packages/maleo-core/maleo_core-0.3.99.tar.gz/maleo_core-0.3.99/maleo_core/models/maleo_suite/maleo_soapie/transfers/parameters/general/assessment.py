from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.soapie import MaleoSOAPIESOAPIEGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers

class MaleoSOAPIEAssessmentGeneralParameters:
    class Expand(BaseModel):
        expand:list[MaleoSOAPIEAssessmentGeneralTransfers.ExpandableFields] = Field([], description="Expanded field(s)")

    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"

    class GetSingle(Expand, BaseGeneralParameters.GetSingle):
        identifier:MaleoSOAPIEAssessmentGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")

    class GetSingleQuery(Expand, BaseGeneralParameters.GetSingleQuery): pass

    class CreateOrUpdate(Expand, MaleoSOAPIESOAPIEGeneralTransfers.SOAPIEID):
        assessment:MaleoSOAPIEAssessmentGeneralTransfers.Base = Field(..., description="Assessment's data")