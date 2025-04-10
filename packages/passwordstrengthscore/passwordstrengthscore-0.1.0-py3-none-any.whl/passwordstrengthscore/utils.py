import math

def count_uppercase(pw: str) -> int:
    return sum(1 for c in pw if c.isupper())

def count_digits(pw: str) -> int:
    return sum(1 for c in pw if c.isdigit())

def has_special_chars(pw: str) -> int:
    return int(any(not c.isalnum() for c in pw))

def calculate_entropy(pw: str) -> float:
    pool_size = 0
    if any(c.islower() for c in pw):
        pool_size += 26
    if any(c.isupper() for c in pw):
        pool_size += 26
    if any(c.isdigit() for c in pw):
        pool_size += 10
    if any(not c.isalnum() for c in pw):
        pool_size += 32  # Approximate number of special characters

    if pool_size == 0:
        return 0.0

    entropy = len(pw) * math.log2(pool_size)
    return round(entropy, 2)
