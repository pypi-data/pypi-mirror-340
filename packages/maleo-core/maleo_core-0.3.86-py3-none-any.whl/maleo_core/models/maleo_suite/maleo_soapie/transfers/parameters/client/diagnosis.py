from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.assessment import MaleoSOAPIEAssessmentGeneralParameters

class MaleoSOAPIEDiagnosisClientParameters:
    class Get(
        MaleoSOAPIEAssessmentGeneralParameters.AssessmentIDs,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoSOAPIEAssessmentGeneralParameters.AssessmentIDs,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass