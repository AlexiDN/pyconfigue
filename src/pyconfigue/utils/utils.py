from typing import Any, Union, get_args, get_origin


def is_optional(tp: type[Any]) -> bool:
    """Check if a type allows None using | None or Union[..., None]"""
    origin = get_origin(tp)
    if origin is Union:
        return type(None) in get_args(tp)
    return origin is type(None)
