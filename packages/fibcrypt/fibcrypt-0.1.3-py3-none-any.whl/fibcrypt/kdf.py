import time
from fibcrypt.fib import fibonacci_mod
from fibcrypt.utils import hash_to_int

def derive_key(password: str, salt: str, iterations: int = 1000, prime: int = 65537) -> int:
    # Derives a cryptographic key using a Fibonacci-based PRNG mechanism
    start_time = time.time()
    seed = hash_to_int(password + salt) % (10**6)
    seed_time = time.time()
    key = 0
    for i in range(iterations):
        key ^= fibonacci_mod(seed + i, prime)  # XOR folding of PRNG outputs
    end_time = time.time()
    print(f"[⏱️] KDF seed hashing time: {seed_time - start_time:.4f} s")
    print(f"[⏱️] KDF Fibonacci loop time: {end_time - seed_time:.4f} s")
    print(f"[⏱️] KDF total time: {end_time - start_time:.4f} s")
    return key