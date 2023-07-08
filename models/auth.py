from pydantic import BaseModel, constr
from models.base import SuccessResponse
from models.users import User


class MeResponse(BaseModel):
    token: str
    me: User


class MeSuccessResponse(SuccessResponse):
    data: MeResponse


class SignUp(BaseModel):
    name: constr(min_length=4)
    password: constr(min_length=8)

class SignIn(SignUp):
    ...