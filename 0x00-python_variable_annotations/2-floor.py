#!/usr/bin/env python3
"""
A  type-annotated function floor which takes a float floorNumber as
argument and returns the floor of the float.
"""
import math


def floor(floorNumber: float) -> int:
    """ Returns a lower bound rounded figure of a float """
    return math.floor(floorNumber)
