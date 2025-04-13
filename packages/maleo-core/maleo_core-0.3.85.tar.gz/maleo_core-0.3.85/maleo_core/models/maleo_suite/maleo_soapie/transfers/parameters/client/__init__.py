# This file serves all MaleoSOAPIE's Cient Parameters

from __future__ import annotations
from .subjective import MaleoSOAPIESubjectiveClientParameters
from .objective import MaleoSOAPIEObjectiveClientParameters
from .vital_sign import MaleoSOAPIEVitalSignClientParameters
from .assessment import MaleoSOAPIEAssessmentClientParameters
from .diagnosis import MaleoSOAPIEDiagnosisClientParameters
from .plan import MaleoSOAPIEPlanClientParameters
from .intervention import MaleoSOAPIEInterventionClientParameters
from .evaluation import MaleoSOAPIEEvaluationClientParameters

class MaleoSOAPIEClientParameters:
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
    "MaleoSOAPIESubjectiveClientParameters",
    "MaleoSOAPIEObjectiveClientParameters",
    "MaleoSOAPIEVitalSignClientParameters",
    "MaleoSOAPIEAssessmentClientParameters",
    "MaleoSOAPIEDiagnosisClientParameters",
    "MaleoSOAPIEPlanClientParameters",
    "MaleoSOAPIEInterventionClientParameters",
    "MaleoSOAPIEEvaluationClientParameters"
]