import os
import time
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from fibcrypt.kdf import derive_key

def int_to_bytes(val: int, length: int) -> bytes:
    # Converts an integer to a byte array of given length
    return val.to_bytes(length, byteorder='big')

def encrypt(plaintext: str, password: str, salt: str, iterations: int = 1000, prime: int = 65537) -> bytes:
    # Encrypts plaintext using AES-256-CBC and a Fibonacci-based derived key
    t0 = time.time()
    seed_gen_start = time.time()
    key_int = derive_key(password, salt, iterations, prime)
    seed_gen_end = time.time()
    key = int_to_bytes(key_int, 32)
    key_convert_end = time.time()

    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    encrypt_end = time.time()

    print(f"[⏱️] KDF time:         {seed_gen_end - seed_gen_start:.4f} s")
    print(f"[⏱️] Key conversion:   {key_convert_end - seed_gen_end:.4f} s")
    print(f"[⏱️] AES encryption:   {encrypt_end - key_convert_end:.4f} s")
    print(f"[⏱️] Total time:       {encrypt_end - t0:.4f} s")
    return iv + ciphertext

def decrypt(ciphertext: bytes, password: str, salt: str, iterations: int = 1000, prime: int = 65537) -> str:
    # Decrypts ciphertext using AES-256-CBC and a Fibonacci-based derived key
    t0 = time.time()
    seed_gen_start = time.time()
    key_int = derive_key(password, salt, iterations, prime)
    seed_gen_end = time.time()
    key = int_to_bytes(key_int, 32)
    key_convert_end = time.time()

    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ct), AES.block_size)
    decrypt_end = time.time()

    print(f"[⏱️] KDF time:         {seed_gen_end - seed_gen_start:.4f} s")
    print(f"[⏱️] Key conversion:   {key_convert_end - seed_gen_end:.4f} s")
    print(f"[⏱️] AES decryption:   {decrypt_end - key_convert_end:.4f} s")
    print(f"[⏱️] Total time:       {decrypt_end - t0:.4f} s")
    return plaintext.decode()
