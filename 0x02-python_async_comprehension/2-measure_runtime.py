#!/usr/bin/env python3
"""
async_comprehension imported from previous task,
execute it 4 times in parallel
"""
import asyncio
import time


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Returns the total runtime"""
    start = time.perf_counter()
    result = await asyncio.gather(*(async_comprehension() for _ in range(4)))
    total = time.perf_counter() - start
    return total
