#!/usr/bin/env python3


import asyncio
import random
import time
from typing import List


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int = 10) -> float:
    """
    returns total_time / n then takes max_delay as  input
    """
    start_time = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    time_elapsed = time.perf_counter() - start_time
    return time_elapsed / n
