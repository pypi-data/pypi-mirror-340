# This file serves all MaleoSOAPIE's General Transfers

from __future__ import annotations
from .soapie import MaleoSOAPIESOAPIEGeneralTransfers
from .subjective import MaleoSOAPIESubjectiveGeneralTransfers
from .objective import MaleoSOAPIEObjectiveGeneralTransfers
from .vital_sign import MaleoSOAPIEVitalSignGeneralTransfers
from .assessment import MaleoSOAPIEAssessmentGeneralTransfers
from .diagnosis import MaleoSOAPIEDiagnosisGeneralTransfers
from .plan import MaleoSOAPIEPlanGeneralTransfers
from .intervention import MaleoSOAPIEInterventionGeneralTransfers
from .evaluation import MaleoSOAPIEEvaluationGeneralTransfers

class MaleoSOAPIEGeneralTransfers:
    SOAPIE = MaleoSOAPIESOAPIEGeneralTransfers
    Subjective = MaleoSOAPIESubjectiveGeneralTransfers
    Objective = MaleoSOAPIEObjectiveGeneralTransfers
    VitalSign = MaleoSOAPIEVitalSignGeneralTransfers
    Assessment = MaleoSOAPIEAssessmentGeneralTransfers
    Diagnosis = MaleoSOAPIEDiagnosisGeneralTransfers
    Plan = MaleoSOAPIEPlanGeneralTransfers
    Intervention = MaleoSOAPIEInterventionGeneralTransfers
    Evaluation = MaleoSOAPIEEvaluationGeneralTransfers

__all__ = [
    "MaleoSOAPIEGeneralTransfers",
    "MaleoSOAPIESOAPIEGeneralTransfers",
    "MaleoSOAPIESubjectiveGeneralTransfers",
    "MaleoSOAPIEObjectiveGeneralTransfers",
    "MaleoSOAPIEAssessmentGeneralTransfers",
    "MaleoSOAPIEDiagnosisGeneralTransfers",
    "MaleoSOAPIEPlanGeneralTransfers",
    "MaleoSOAPIEInterventionGeneralTransfers",
    "MaleoSOAPIEEvaluationGeneralTransfers"
]