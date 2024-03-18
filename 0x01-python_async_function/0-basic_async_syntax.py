#!/usr/bin/env python3
"""
This a module for creating the wait_random function
and then initialize the argument, max_delay with an initial value of 10
"""

import asyncio
import random


async def wait_random(max_delay: int=10) -> float:
    "This function initializes the value of max_delay"
    delay: float = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
