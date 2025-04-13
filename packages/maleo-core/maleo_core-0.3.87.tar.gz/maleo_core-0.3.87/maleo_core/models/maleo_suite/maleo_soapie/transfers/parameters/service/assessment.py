from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.soapie import MaleoSOAPIESOAPIEGeneralParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.assessment import MaleoSOAPIEAssessmentGeneralParameters

class MaleoSOAPIEAssessmentServiceParameters:
    class GetQuery(
        MaleoSOAPIEAssessmentGeneralParameters.Expand,
        MaleoSOAPIESOAPIEGeneralParameters.SOAPIEIDs,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoSOAPIEAssessmentGeneralParameters.Expand,
        MaleoSOAPIESOAPIEGeneralParameters.SOAPIEIDs,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass