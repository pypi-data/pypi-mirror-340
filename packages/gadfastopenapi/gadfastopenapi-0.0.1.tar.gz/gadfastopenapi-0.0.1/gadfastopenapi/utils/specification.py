import typing

from gadfastopenapi import const


def findrefs(openapi: typing.Union[typing.Dict, typing.List], find: str, replace: str) -> None:
    if isinstance(openapi, typing.Dict):
        for key, value in openapi.items():
            if (
                key == const.SPECIFICATION_COMPONENTS_SCHEMAS_REF_KEY
                and value == f"{const.SPECIFICATION_COMPONENTS_SCHEMAS_REF_PATH}{find}"
            ):
                openapi[key] = f"{const.SPECIFICATION_COMPONENTS_SCHEMAS_REF_PATH}{replace}"
            else:
                findrefs(value, find, replace)
    elif isinstance(openapi, typing.List):
        for item in openapi:
            findrefs(item, find, replace)


__all__ = ["findrefs"]
