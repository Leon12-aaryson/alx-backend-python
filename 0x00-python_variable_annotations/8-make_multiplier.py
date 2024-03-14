#!/usr/bin/env python3
"""
Write a type-annotated function make_multiplier that takes a float
multiplier as argument and returns a function that multiplies a
float by multiplier
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ Returns a multiplier function """

    def multiplier_func(number: float) -> float:
        """ Multiplies by the number"""
        return multiplier * number

    return multiplier_func
