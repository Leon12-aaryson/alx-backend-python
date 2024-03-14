#!/usr/bin/env python3
"""
Added type annotations to the function.
"""
from typing import Any, Optional, TypeVar, Union, Mapping

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default:
                     Optional[T] = None) -> Union[Any, T]:
    """ Return default or dict value"""
    if key in dct:
        return dct[key]
    else:
        return default
