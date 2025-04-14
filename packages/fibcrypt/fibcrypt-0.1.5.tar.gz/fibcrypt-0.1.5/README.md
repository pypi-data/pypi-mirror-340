# fibcrypt

**fibcrypt** is a lightweight, open-source cryptographic toolkit based on fast Fibonacci number generation using matrix exponentiation.

## 🔐 Features

- Fast Fibonacci-based PRNG (O(log n))
- AES-256 encryption & decryption (CBC mode)
- Custom key derivation function (KDF)
- Modular, pluggable and extensible structure
- Built-in performance profiling

## 📦 Installation

```bash
pip install fibcrypt
```

## 🚀 Example Usage
```python
from fibcrypt.crypto_utils import encrypt, decrypt

msg = "This is a secret message"
password = "myStrongPassword123"
salt = "user@example.com"

# Encrypt
cipher = encrypt(msg, password, salt)
print("Encrypted:", cipher.hex())

# Decrypt
plain = decrypt(cipher, password, salt)
print("Decrypted:", plain)
```
## 📈 Performance Example
Google Colab Notebook: https://colab.research.google.com/drive/14Rj_vPUbSV4-qcRi2jur-YMa7rF1P03B?usp=sharing
- [⏱️] KDF total time: 0.0625 s
- [⏱️] AES encryption: 0.0001 s
- [⏱️] Total time:     0.0626 s

## 🛡️ License
This project is licensed under the MIT License - feel free to use and contribute!

