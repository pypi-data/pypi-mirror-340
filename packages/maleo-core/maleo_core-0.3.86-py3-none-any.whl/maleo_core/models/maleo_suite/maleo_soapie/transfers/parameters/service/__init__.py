# This file serves all MaleoSOAPIE's Service Parameters

from __future__ import annotations
from .soapie import MaleoSOAPIESOAPIEServiceParameters
from .subjective import MaleoSOAPIESubjectiveServiceParameters
from .objective import MaleoSOAPIEObjectiveServiceParameters
from .vital_sign import MaleoSOAPIEVitalSignServiceParameters
from .assessment import MaleoSOAPIEAssessmentServiceParameters
from .diagnosis import MaleoSOAPIEDiagnosisServiceParameters
from .plan import MaleoSOAPIEPlanServiceParameters
from .intervention import MaleoSOAPIEInterventionServiceParameters
from .evaluation import MaleoSOAPIEEvaluationServiceParameters

class MaleoSOAPIEServiceParameters:
    SOAPIE = MaleoSOAPIESOAPIEServiceParameters
    Subjective = MaleoSOAPIESubjectiveServiceParameters
    Objective = MaleoSOAPIEObjectiveServiceParameters
    VitalSign = MaleoSOAPIEVitalSignServiceParameters
    Assessment = MaleoSOAPIEAssessmentServiceParameters
    Diagnosis = MaleoSOAPIEDiagnosisServiceParameters
    Plan = MaleoSOAPIEPlanServiceParameters
    Intervention = MaleoSOAPIEInterventionServiceParameters
    Evaluation = MaleoSOAPIEEvaluationServiceParameters

__all__ = [
    "MaleoSOAPIEServiceParameters",
    "MaleoSOAPIESOAPIEServiceParameters",
    "MaleoSOAPIESubjectiveServiceParameters",
    "MaleoSOAPIEObjectiveServiceParameters",
    "MaleoSOAPIEVitalSignServiceParameters",
    "MaleoSOAPIEAssessmentServiceParameters",
    "MaleoSOAPIEDiagnosisServiceParameters",
    "MaleoSOAPIEPlanServiceParameters",
    "MaleoSOAPIEInterventionServiceParameters",
    "MaleoSOAPIEEvaluationServiceParameters"
]