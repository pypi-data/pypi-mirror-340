import inspect

from vkbottle_types.codegen.responses.wall import *  # noqa: F403,F401

from .base_response import BaseResponse


class WallGetByIdExtendedResponseModel(WallGetByIdExtendedResponseModel):  # type: ignore[no-redef]
    items: typing.List["WallWallpostFull"] = Field()


class WallGetByIdExtendedResponse(WallGetByIdExtendedResponse):  # type: ignore[no-redef]
    response: "WallGetByIdExtendedResponseModel" = Field()


class WallGetByIdResponseModel(WallGetByIdResponseModel):  # type: ignore[no-redef]
    items: typing.Optional[typing.List["WallWallpostFull"]] = Field(
        default=None,
    )


class WallGetByIdResponse(WallGetByIdResponse):  # type: ignore[no-redef]
    response: "WallGetByIdResponseModel" = Field()


class WallGetExtendedResponseModel(WallGetExtendedResponseModel):  # type: ignore[no-redef]
    items: typing.List["WallWallpostFull"] = Field()


class WallGetExtendedResponse(WallGetExtendedResponse):  # type: ignore[no-redef]
    response: "WallGetExtendedResponseModel" = Field()


class WallGetResponseModel(WallGetResponseModel):  # type: ignore[no-redef]
    items: typing.List["WallWallpostFull"] = Field()


class WallGetResponse(WallGetResponse):  # type: ignore[no-redef]
    response: "WallGetResponseModel" = Field()


class WallSearchExtendedResponseModel(WallSearchExtendedResponseModel):  # type: ignore[no-redef]
    items: typing.List["WallWallpostFull"] = Field()


class WallSearchExtendedResponse(WallSearchExtendedResponse):  # type: ignore[no-redef]
    response: "WallSearchExtendedResponseModel" = Field()


class WallSearchResponseModel(WallSearchResponseModel):  # type: ignore[no-redef]
    items: typing.List["WallWallpostFull"] = Field()


class WallSearchResponse(WallSearchResponse):  # type: ignore[no-redef]
    response: "WallSearchResponseModel" = Field()


_locals = locals().copy()
_locals_values = _locals.values()
for item in _locals_values:
    if not (inspect.isclass(item) and issubclass(item, BaseResponse)):
        continue
    item.update_forward_refs(**_locals)
    for parent in item.__bases__:
        if parent.__name__ == item.__name__:
            parent.__fields__.update(item.__fields__)  # type: ignore
            parent.update_forward_refs(**_locals)  # type: ignore
