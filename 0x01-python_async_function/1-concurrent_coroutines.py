#!/usr/bin/env python3
"""_summary_
"""

from typing import List
import asyncio
import random


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """ Returns list of all delays(floats) in ASC order """
    tosoList = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    return [await todo for todo in asyncio.as_completed(tosoList)]
