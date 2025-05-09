import secrets
import string
import hashlib
import math

# === ENTROPY CONFIGURATION CONSTANTS ===
PASSWORD_LENGTH = 16  # Length of the password
USE_UPPERCASE = True
USE_LOWERCASE = True
USE_DIGITS = True
USE_SYMBOLS = True
USE_HASH_SALT = False  # Optional: Append a hashed salt to increase complexity

# === CHARACTER SET POOL BASED ON SETTINGS ===
CHAR_POOL = ''
if USE_LOWERCASE:
    CHAR_POOL += string.ascii_lowercase
if USE_UPPERCASE:
    CHAR_POOL += string.ascii_uppercase
if USE_DIGITS:
    CHAR_POOL += string.digits
if USE_SYMBOLS:
    CHAR_POOL += string.punctuation

# === FUNCTION TO CALCULATE THEORETICAL ENTROPY ===
def calculate_entropy(length: int, pool_size: int) -> float:
    return length * math.log2(pool_size)

# === PASSWORD GENERATOR ===
def generate_password(length=PASSWORD_LENGTH) -> str:
    if not CHAR_POOL:
        raise ValueError("Character pool is empty. Enable at least one character type.")
    
    password = ''.join(secrets.choice(CHAR_POOL) for _ in range(length))

    # Optional salt & hash extension
    if USE_HASH_SALT:
        salt = secrets.token_bytes(8)
        hash_digest = hashlib.sha256(password.encode('utf-8') + salt).hexdigest()[:8]
        password += hash_digest

    entropy = calculate_entropy(len(password), len(CHAR_POOL))
    print(f"Generated Password: {password}")
    print(f"Entropy: {entropy:.2f} bits")

    return password

# === MAIN EXECUTION ===
if __name__ == "__main__":
    
    generate_password()
