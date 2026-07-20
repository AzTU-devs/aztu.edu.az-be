from typing import Annotated, List, Optional

from pydantic import BaseModel, BeforeValidator, Field

from app.api.v1.schema.common import OptionalInt, OptionalStr, blank_to_none

# Admin <select>/<input> submit "" for untouched fields; without this a bool field
# left blank raises a 422 instead of meaning "unchanged".
OptionalBool = Annotated[Optional[bool], BeforeValidator(blank_to_none)]

PASSWORD_MIN_LENGTH = 8


class RoleCreate(BaseModel):
    code: str = Field(min_length=2, max_length=50, pattern=r"^[a-z][a-z0-9_]*$")
    name_az: str = Field(min_length=1, max_length=100)
    name_en: str = Field(min_length=1, max_length=100)
    description: OptionalStr = None
    permissions: List[str] = []


class RoleUpdate(BaseModel):
    name_az: OptionalStr = None
    name_en: OptionalStr = None
    description: OptionalStr = None


class RolePermissionsUpdate(BaseModel):
    permissions: List[str] = []


class AdminUserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9._-]+$")
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=128)
    first_name: OptionalStr = Field(default=None, max_length=100)
    last_name: OptionalStr = Field(default=None, max_length=100)
    role_id: OptionalInt = None
    is_active: OptionalBool = True


class AdminUserUpdate(BaseModel):
    username: OptionalStr = Field(default=None, max_length=50)
    first_name: OptionalStr = Field(default=None, max_length=100)
    last_name: OptionalStr = Field(default=None, max_length=100)
    is_active: OptionalBool = None


class AdminUserRoleAssign(BaseModel):
    role_id: int


class AdminUserPasswordReset(BaseModel):
    password: str = Field(min_length=PASSWORD_MIN_LENGTH, max_length=128)
