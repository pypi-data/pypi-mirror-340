from __future__ import annotations
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user import MaleoAccessUserQueryResults

class MaleoAccessAuthorizationServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class Login(BaseServiceGeneralResults.SingleData):
        data:MaleoAccessUserQueryResults.Get

    class Logout(BaseServiceGeneralResults.SingleData):
        data:None