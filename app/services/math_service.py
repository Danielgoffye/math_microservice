import redis
import os

# Citim hostul din variabilă de mediu (setată în docker-compose.yml)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    db=0,
    decode_responses=True
)

# -------------------- POW --------------------


def _pow_logic(base: int, exponent: int) -> int:
    return base ** exponent


def compute_pow(base: int, exponent: int) -> tuple[int, int]:
    key = f"pow:{base}:{exponent}"
    cached = redis_client.get(key)
    if cached is not None:
        print(f"[REDIS CACHE HIT] pow({base}, {exponent})")
        return int(cached), 1  # result, was_cached

    result = _pow_logic(base, exponent)
    redis_client.set(key, result)
    return result, 0

# -------------------- FACTORIAL --------------------


def _factorial_logic(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def compute_factorial(n: int) -> tuple[int, int]:
    key = f"fact:{n}"
    cached = redis_client.get(key)
    if cached is not None:
        print(f"[REDIS CACHE HIT] factorial({n})")
        return int(cached), 1

    result = _factorial_logic(n)
    redis_client.set(key, result)
    return result, 0

# -------------------- FIBONACCI --------------------


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


def compute_fibonacci(n: int) -> tuple[int, int]:
    key = f"fib:{n}"
    cached = redis_client.get(key)
    if cached is not None:
        print(f"[REDIS CACHE HIT] fibonacci({n})")
        return int(cached), 1

    result = _fibonacci_logic(n)
    redis_client.set(key, result)
    return result, 0
