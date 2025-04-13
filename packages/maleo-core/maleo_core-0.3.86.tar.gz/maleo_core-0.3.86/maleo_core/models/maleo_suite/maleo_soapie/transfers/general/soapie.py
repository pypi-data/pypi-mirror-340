from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.subjective import MaleoSOAPIESubjectiveGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.objective import MaleoSOAPIEObjectiveGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.assessment import MaleoSOAPIEAssessmentGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.plan import MaleoSOAPIEPlanGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.intervention import MaleoSOAPIEInterventionGeneralTransfers
from maleo_core.models.maleo_suite.maleo_soapie.transfers.general.evaluation import MaleoSOAPIEEvaluationGeneralTransfers

class MaleoSOAPIESOAPIEGeneralTransfers:
    class Base(BaseModel):
        subjective:Optional[MaleoSOAPIESubjectiveGeneralTransfers.Base] = Field(None, description="Subjective")
        objective:Optional[MaleoSOAPIEObjectiveGeneralTransfers.Base] = Field(None, description="Objective")
        assessment:Optional[MaleoSOAPIEAssessmentGeneralTransfers.Base] = Field(None, description="Assessment")
        plan:Optional[MaleoSOAPIEPlanGeneralTransfers.Base] = Field(None, description="Plan")
        intervention:Optional[MaleoSOAPIEInterventionGeneralTransfers.Base] = Field(None, description="Intervention")
        evaluation:Optional[MaleoSOAPIEEvaluationGeneralTransfers.Base] = Field(None, description="Evaluation")