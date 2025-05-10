import math
import string
import re

# === Configuration ===
MAX_LENGTH = 15
MIN_LENGTH = 10
MIN_ENTROPY = 60
DICTIONARY_FILE = "rockyou.txt"
CSV_FILE = "example_list.csv"


from guess_factor import guessability_from_personal_history, load_personal_passwords


def load_dictionary(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Dictionary check skipped.")
        return set()


dictionary_words = load_dictionary(DICTIONARY_FILE)

# === Entropy Calculation ===



def calculate_entropy(password: str) -> float:
    unique_chars = len(set(password))
    return len(password) * math.log2(unique_chars) if unique_chars > 1 else 0

# === Checks ===
def has_variety(password: str) -> bool:
    categories = [
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ]
    return sum(categories) >= 3  # Must contain at least 3 of 4

def has_predictable_pattern(password: str) -> bool:
    patterns = ["123", "abc", "000", "111", "aaa", "qwerty"]
    for p in patterns:
        if p in password.lower():
            return True
    if re.search(r'(.)\1{2,}', password):  # repeated characters like $$$ or aaa
        return True
    return False

def is_dictionary_resistant(password: str) -> bool:
    pw_lower = password.lower()
    if pw_lower in dictionary_words:
        return False  # 🔥 Penalize if exact match found in rocky.txt

    score = 0
    if any(c in string.punctuation for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if len(set(password)) > 8:
        score += 1
    return score >= 2  # Needs at least 2 signs of randomness


# === Scoring Function ===
def evaluate_password(password: str):
    score = 0
    reasons = []

    entropy = calculate_entropy(password)
    print(f"\nPassword: {password}")
    print(f"Entropy: {entropy:.2f} bits")

    # Entropy Score
    if entropy >= MIN_ENTROPY:
        score += 1
    else:
        reasons.append("Entropy too low")

    # Variety Score
    if has_variety(password):
        score += 1
    else:
        reasons.append("Lacks variety (upper/lower/digits/symbols)")

    # Usability Score
    if MIN_LENGTH <= len(password) <= MAX_LENGTH:
        score += 1
    else:
        reasons.append("Too long or too short")

    # Dictionary Attack Resistance Score (inferred)
    if is_dictionary_resistant(password):
        score += 1
    else:
        reasons.append("Too basic, likely guessable")

    # Personal Guessability Check (replaces pattern check)
    past_passwords, pw_to_site = load_personal_passwords(CSV_FILE)
    guessability, matched_pw = guessability_from_personal_history(password, past_passwords)
    if guessability.startswith("LOW"):
        score += 1
    elif guessability.startswith("MEDIUM"):
        score += 0.5  # partial credit
    
    # Reason logging
    if guessability.startswith("HIGH") or guessability.startswith("MEDIUM"):
        website = pw_to_site.get(matched_pw, "unknown site")
        reasons.append(f"Too similar to password used on {website}")

    # Pattern Check
    if not has_predictable_pattern(password):
        score += 1
    else:
        reasons.append("Has predictable pattern")

        
 

    # Final Score Report
    print(f"Security Score: {score}/6")

    if score == 6:
        print("Excellent! Very Strong and practical password.")
    elif score >= 5:
        print("Good!")
    elif score >= 3:
        print("Moderate. Could use some hardening ")
    else:
        print(" Weak. Avoid using this password.")

    if reasons:
        print("Suggestions:")
        for r in reasons:
            print(f"- {r}")

# === Main Execution ===
if __name__ == "__main__":
    test_password = input("Enter password to evaluate: ")

    evaluate_password(test_password)
