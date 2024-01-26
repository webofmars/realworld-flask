from realworld.api.core.models import BaseCamelModel

#
# Response Model
#

class TagsResponse(BaseCamelModel):
    tags: list[str]
