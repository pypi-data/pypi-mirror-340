from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.soapie import MaleoSOAPIESOAPIEGeneralParameters

class MaleoSOAPIEPlanClientParameters:
    class Get(
        MaleoSOAPIESOAPIEGeneralParameters.SOAPIEIDs,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoSOAPIESOAPIEGeneralParameters.SOAPIEIDs,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass