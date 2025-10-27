"""
password_analyzer.py
Provides password strength evaluation using zxcvbn plus a simple entropy estimate.
"""

from zxcvbn import zxcvbn
import math

def estimate_entropy(password: str) -> float:
    """
    Rough entropy estimate:
    Use character class sizes (lower, upper, digits, symbols) heuristic.
    This is not perfect but provides an extra viewpoint.
    """
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() for c in password):
        pool += 32  # rough symbol count
    if pool == 0:
        return 0.0
    entropy = math.log2(pool) * len(password)
    return entropy

def analyze(password: str, user_inputs: list[str] | None = None) -> dict:
    """
    Returns a dictionary with zxcvbn result plus entropy.
    user_inputs: optional list of strings to pass as user_inputs to zxcvbn (personal info)
    """
    user_inputs = user_inputs or []
    zx = zxcvbn(password, user_inputs=user_inputs)
    entropy = estimate_entropy(password)
    # Add entropy to result
    zx['estimated_entropy'] = entropy
    # Map score to text
    score_map = {
        0: "Very weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very strong"
    }
    zx['strength_text'] = score_map.get(zx.get('score', 0), "Unknown")
    return zx

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Analyze a password")
    parser.add_argument("password", help="Password to analyze")
    parser.add_argument("--user", "-u", action="append", help="User inputs (name, pet, etc.). Can be used multiple times.")
    args = parser.parse_args()
    res = analyze(args.password, user_inputs=args.user)
    print(json.dumps(res, indent=2))
