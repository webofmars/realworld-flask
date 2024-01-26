from realworld.api.core.models import BaseCamelModel, Profile


class SingleProfileResponse(BaseCamelModel):
    profile: Profile
