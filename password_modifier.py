import secrets
import string
import math

# === MODIFICATION CONFIGURATION ===
REPLACE_LETTERS = True
APPEND_SYMBOL = True
INSERT_RANDOM_UPPERCASE = True
ADD_NUMBER_SUFFIX = True
SHOW_ENTROPY = True

# === TUNING SYMBOLS/REPLACEMENTS === most used letters so chances of replacemnet are high
LETTER_SUBS = {
    'a': '@', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '!',
    'o': '0', 'O': '0',
    's': '$', 'S': '5'
}
SYMBOLS = "!@#$%^&*()_+-=[]{}"

def calculate_entropy(password: str) -> float:
    unique_chars = len(set(password))
    return len(password) * math.log2(unique_chars) if unique_chars > 1 else 0

def modify_password(base: str) -> str:
    modified = list(base)

    # Replace common letters
    if REPLACE_LETTERS:
        modified = [LETTER_SUBS.get(c, c) for c in modified]
        #print(modified)

    # Insert a random uppercase letter at a random position
    if INSERT_RANDOM_UPPERCASE:
        pos = secrets.randbelow(len(modified) + 1)
        modified.insert(pos, secrets.choice(string.ascii_uppercase))

    # Append a random symbol
    if APPEND_SYMBOL:
        modified.append(secrets.choice(SYMBOLS))

    # Add a random 2-digit number suffix
    if ADD_NUMBER_SUFFIX:
        modified.append(str(secrets.randbelow(90) + 10))  # 10–99

    final_password = ''.join(modified)
    if SHOW_ENTROPY:
        entropy = calculate_entropy(final_password)
        print(f"Modified Password: {final_password}")
        print(f"Estimated Entropy: {entropy:.2f} bits")

    return final_password

# === MAIN EXECUTION ===
if __name__ == "__main__":
    # EXAMPLE: You can change this to input() if you want user input
    base_password = input("Enter password to evaluate: ")
    modify_password(base_password)


