# This file serves all MaleoSOAPIE's Cient Parameters

from __future__ import annotations
from .soapie import MaleoSOAPIESOAPIEClientParameters
from .subjective import MaleoSOAPIESubjectiveClientParameters
from .objective import MaleoSOAPIEObjectiveClientParameters
from .vital_sign import MaleoSOAPIEVitalSignClientParameters
from .assessment import MaleoSOAPIEAssessmentClientParameters
from .diagnosis import MaleoSOAPIEDiagnosisClientParameters
from .plan import MaleoSOAPIEPlanClientParameters
from .intervention import MaleoSOAPIEInterventionClientParameters
from .evaluation import MaleoSOAPIEEvaluationClientParameters

class MaleoSOAPIEClientParameters:
    SOAPIE = MaleoSOAPIESOAPIEClientParameters
    Subjective = MaleoSOAPIESubjectiveClientParameters
    Objective = MaleoSOAPIEObjectiveClientParameters
    VitalSign = MaleoSOAPIEVitalSignClientParameters
    Assessment = MaleoSOAPIEAssessmentClientParameters
    Diagnosis = MaleoSOAPIEDiagnosisClientParameters
    Plan = MaleoSOAPIEPlanClientParameters
    Intervention = MaleoSOAPIEInterventionClientParameters
    Evaluation = MaleoSOAPIEEvaluationClientParameters

__all__ = [
    "MaleoSOAPIEClientParameters",
    "MaleoSOAPIESOAPIEClientParameters",
    "MaleoSOAPIESubjectiveClientParameters",
    "MaleoSOAPIEObjectiveClientParameters",
    "MaleoSOAPIEVitalSignClientParameters",
    "MaleoSOAPIEAssessmentClientParameters",
    "MaleoSOAPIEDiagnosisClientParameters",
    "MaleoSOAPIEPlanClientParameters",
    "MaleoSOAPIEInterventionClientParameters",
    "MaleoSOAPIEEvaluationClientParameters"
]