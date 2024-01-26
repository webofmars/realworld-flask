from realworld.api.core.models import BaseCamelModel, User

#
# Request Models
#

class CreateUserData(BaseCamelModel):
    username: str
    email: str
    password: str


class CreateUserRequest(BaseCamelModel):
    user: CreateUserData


class UpdateUserRequest(BaseCamelModel):
    user: User


class AuthenticateUserRequest(BaseCamelModel):
    email: str
    password: str


#
# Response Models
#

class SingleUserResponse(BaseCamelModel):
    user: User
