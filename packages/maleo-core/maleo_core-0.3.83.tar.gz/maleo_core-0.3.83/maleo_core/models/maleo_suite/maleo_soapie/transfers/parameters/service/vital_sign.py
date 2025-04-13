from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_soapie.transfers.parameters.general.objective import MaleoSOAPIEObjectiveGeneralParameters

class MaleoSOAPIEVitalSignServiceParameters:
    class GetQuery(
        MaleoSOAPIEObjectiveGeneralParameters.ObjectiveIDs,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoSOAPIEObjectiveGeneralParameters.ObjectiveIDs,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass