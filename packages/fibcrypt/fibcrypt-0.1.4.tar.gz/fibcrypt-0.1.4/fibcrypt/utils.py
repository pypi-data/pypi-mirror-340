import hashlib

def hash_to_int(data: str) -> int:
    # Hashes the input string with SHA-256 and converts the result to an integer
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)