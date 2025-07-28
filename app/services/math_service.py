# app/services/math_service.py
from functools import lru_cache


def _pow_logic(base: int, exponent: int) -> int:
    return base ** exponent


@lru_cache(maxsize=1000)
def _cached_pow(base: int, exponent: int) -> int:
    return _pow_logic(base, exponent)


def compute_pow(base: int, exponent: int) -> int:
    info_before = _cached_pow.cache_info()
    result = _cached_pow(base, exponent)
    info_after = _cached_pow.cache_info()
    if info_before.hits < info_after.hits:
        print(f"[CACHE HIT] pow({base}, {exponent})")
    return result


def _factorial_logic(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@lru_cache(maxsize=1000)
def _cached_factorial(n: int) -> int:
    return _factorial_logic(n)


def compute_factorial(n: int) -> int:
    info_before = _cached_factorial.cache_info()
    result = _cached_factorial(n)
    info_after = _cached_factorial.cache_info()
    if info_before.hits < info_after.hits:
        print(f"[CACHE HIT] factorial({n})")
    return result


def _fibonacci_logic(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers.")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@lru_cache(maxsize=1000)
def _cached_fibonacci(n: int) -> int:
    return _fibonacci_logic(n)


def compute_fibonacci(n: int) -> int:
    info_before = _cached_fibonacci.cache_info()
    result = _cached_fibonacci(n)
    info_after = _cached_fibonacci.cache_info()
    if info_before.hits < info_after.hits:
        print(f"[CACHE HIT] fibonacci({n})")
    return result
