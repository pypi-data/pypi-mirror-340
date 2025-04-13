from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.objective import MaleoSOAPIEObjectiveGeneralParameters

class MaleoSOAPIEVitalSignClientParameters:
    class Get(
        MaleoSOAPIEObjectiveGeneralParameters.ObjectiveIDs,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoSOAPIEObjectiveGeneralParameters.ObjectiveIDs,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass