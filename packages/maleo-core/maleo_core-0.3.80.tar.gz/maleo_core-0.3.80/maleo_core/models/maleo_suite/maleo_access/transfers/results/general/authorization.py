from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class MaleoAccessAuthorizationGeneralResults:
    class BaseLoginData(BaseModel):
        system_role:UUID = Field(..., description="System role's UUID"),
        user:UUID = Field(..., description="user's UUID"),
        organization:Optional[UUID] = Field(None, description="Organization's UUID")
        organization_roles:Optional[list[UUID]] = Field(None, description="Organization Role's UUID")
        token:str = Field("token", description="Access Token")

    class LoginTokens(BaseModel):
        refresh_token:str = Field(..., description="Refresh Token")
        access_token:str = Field(..., description="Access Token")