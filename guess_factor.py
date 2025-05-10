from difflib import SequenceMatcher
from typing import List
import pandas as pd

# === CONFIGURATION ===
LEVENSHTEIN_THRESHOLD = 0.75  # Threshold above which a password is considered too similar
NGRAM_SIZE = 3
JACCARD_THRESHOLD = 0.5

# === HELPER FUNCTIONS ===
def is_levenshtein_similar(pw1: str, pw2: str, threshold: float = LEVENSHTEIN_THRESHOLD) -> bool:
    return SequenceMatcher(None, pw1, pw2).ratio() >= threshold

def ngrams(s: str, n: int = NGRAM_SIZE) -> set:
    return set([s[i:i+n] for i in range(len(s)-n+1)])

def jaccard_similarity(s1: str, s2: str) -> float:
    n1 = ngrams(s1)
    n2 = ngrams(s2)
    if not n1 or not n2:
        return 0.0
    return len(n1 & n2) / len(n1 | n2)

# === MAIN GUESSABILITY FUNCTION ===
def guessability_from_personal_history(new_pw: str, past_pw_list: List[str]) -> tuple:
    new_pw_lower = new_pw.lower()
    for old_pw in past_pw_list:
        old_pw_lower = old_pw.lower()
        lev_score = SequenceMatcher(None, new_pw_lower, old_pw_lower).ratio()
        jac_score = jaccard_similarity(new_pw_lower, old_pw_lower)

        #print(f"Compared to: {old_pw}")
        #print(f"  Levenshtein similarity: {lev_score:.2f}")
        #print(f"  Jaccard similarity:     {jac_score:.2f}")
        
        if lev_score >= LEVENSHTEIN_THRESHOLD:
            return "HIGH (Levenshtein match)", old_pw
        elif jac_score > JACCARD_THRESHOLD:
            return "MEDIUM (n-gram pattern overlap)", old_pw
    
    return "LOW (sufficiently unique)", None


# === FILE LOADER ===

def load_personal_passwords(filepath: str):
    try:
        df = pd.read_csv(filepath, encoding='latin1')
        password_list = df['Password'].dropna().tolist()
        pw_to_site = dict(zip(df['Password'], df['Website']))
        return password_list, pw_to_site
    except FileNotFoundError:
        print(f"[!] File not found: {filepath}")
        return [], {}
    except KeyError:
        print(f"[!] Required columns not found in {filepath}")
        return [], {}

if __name__ == "__main__":
    file_path = "example_list.csv"
    past_passwords, pw_to_site = load_personal_passwords(file_path)

    new_pw = input("Enter a new password to check for personal guessability: ")
    guessability, matched_pw = guessability_from_personal_history(new_pw, past_passwords)

    if matched_pw:
        website = pw_to_site.get(matched_pw, "unknown site")
        print(f"\nPersonal Guessability: {guessability} — similar to password used for {website}")
    else:
        print(f"\nPersonal Guessability: {guessability}")

