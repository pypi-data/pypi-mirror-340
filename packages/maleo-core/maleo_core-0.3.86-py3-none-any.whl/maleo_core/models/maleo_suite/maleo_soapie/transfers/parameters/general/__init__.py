# This file serves all MaleoSOAPIE's General Parameters

from __future__ import annotations
from .soapie import MaleoSOAPIESOAPIEGeneralParameters
from .subjective import MaleoSOAPIESubjectiveGeneralParameters
from .objective import MaleoSOAPIEObjectiveGeneralParameters
from .vital_sign import MaleoSOAPIEVitalSignGeneralParameters
from .assessment import MaleoSOAPIEAssessmentGeneralParameters
from .diagnosis import  MaleoSOAPIEDiagnosisGeneralParameters
from .plan import MaleoSOAPIEPlanGeneralParameters
from .intervention import MaleoSOAPIEInterventionGeneralParameters
from .evaluation import MaleoSOAPIEEvaluationGeneralParameters

class MaleoAcccesGeneralParameters:
    SOAPIE = MaleoSOAPIESOAPIEGeneralParameters
    Subjective = MaleoSOAPIESubjectiveGeneralParameters
    Objective = MaleoSOAPIEObjectiveGeneralParameters
    VitalSign = MaleoSOAPIEVitalSignGeneralParameters
    Assessment = MaleoSOAPIEAssessmentGeneralParameters
    Diagnosis = MaleoSOAPIEDiagnosisGeneralParameters
    Plan = MaleoSOAPIEPlanGeneralParameters
    Intervention = MaleoSOAPIEInterventionGeneralParameters
    Evaluation = MaleoSOAPIEEvaluationGeneralParameters

__all__ = [
    "MaleoAcccesGeneralParameters",
    "MaleoSOAPIESubjectiveGeneralParameters",
    "MaleoSOAPIEObjectiveGeneralParameters",
    "MaleoSOAPIEVitalSignGeneralParameters",
    "MaleoSOAPIEAssessmentGeneralParameters",
    "MaleoSOAPIEDiagnosisGeneralParameters",
    "MaleoSOAPIEPlanGeneralParameters",
    "MaleoSOAPIEInterventionGeneralParameters",
    "MaleoSOAPIEEvaluationGeneralParameters"
]