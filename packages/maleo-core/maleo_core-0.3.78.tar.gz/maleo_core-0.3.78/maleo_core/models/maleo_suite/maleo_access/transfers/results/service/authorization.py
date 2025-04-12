from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user import MaleoAccessUserQueryResults

class MaleoAccessAuthorizationServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class BaseLoginData(BaseModel):
        system_role_id:int = Field(..., description="System role's ID"),
        user_id:int = Field(..., description="user's ID"),
        organization_id:Optional[int] = Field(None, description="Organization's ID")
        organization_role_id:Optional[int] = Field(None, description="Organization Role's ID")
        token:str = Field("token", description="Token")

    class LoginData(BaseModel):
        base: MaleoAccessAuthorizationServiceResults.BaseLoginData
        user:MaleoAccessUserQueryResults.Get

    class Login(BaseServiceGeneralResults.SingleData):
        data:MaleoAccessAuthorizationServiceResults.LoginData

    class Logout(BaseServiceGeneralResults.SingleData):
        data:None