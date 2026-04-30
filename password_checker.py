# ============================================================
# Password Complexity Checker - PRODIGY_CS_03
# ============================================================

import re
import getpass

COMMON_PASSWORDS = [
    "password", "password123", "123456",
    "12345678", "qwerty", "admin",
    "letmein", "welcome", "iloveyou", "monkey"
]

BAD_SEQUENCES = [
    "123", "234", "345", "456", "567",
    "678", "789", "abc", "bcd", "cde",
    "qwe", "asd"
]


def check_password(password):
    score = 0
    warnings = []
    suggestions = []

    # Length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        suggestions.append("Use a longer password — 12 or more characters is ideal.")
    else:
        suggestions.append("Your password is too short. Use at least 8 characters.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter (A–Z).")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter (a–z).")

    # Number
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Include at least one number (0–9).")

    # Special character
    if re.search(r"[!@#$%^&*()\-_=+\[\]{};:,.<>?/`~]", password):
        score += 1
    else:
        suggestions.append("Add a special character (e.g., ! @ # $ % ^ & *).")

    score = min(score, 6)

    # SECURITY CHECKS

    # Common password
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        warnings.append("This is a commonly used password. Please choose a unique one.")
        suggestions = []

    # Repetition
    if re.search(r"(.)\1{2,}", password):
        score = max(0, score - 2)
        warnings.append("Avoid repeating characters like 'aaa' or '111'.")

    # Sequence
    if any(seq in password.lower() for seq in BAD_SEQUENCES):
        score = max(0, score - 1)
        warnings.append("Avoid simple patterns like '123' or 'abc'.")

    # Strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return score, strength, suggestions, warnings


def draw_meter(score, max_score=6, width=20):
    filled = round(width * score / max_score)
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]  " + str(score) + "/" + str(max_score)


def show_results(password, score, strength, suggestions, warnings):
    print("\n" + "=" * 48)
    print("  RESULT")
    print("=" * 48)
    print(f"  Password : {'*' * len(password)} ({len(password)} characters)")
    print(f"  Strength : {strength}")
    print(f"  Meter    : {draw_meter(score)}")
    print("  Note     : Score is based on 6 basic checks")

    # Show warnings only if they exist
    if warnings:
        print("\n  ⚠ Security Warnings:")
        for w in warnings:
            print("  ! " + w)

    # Suggestions
    print("\n  How to improve:")
    if suggestions:
        for tip in suggestions[:4]:
            print("  -> " + tip)
    else:
        print("  -> No improvements needed based on basic checks.")

    # Strong message
    if strength == "Strong" and not warnings:
        print("\n  ✅ Great password! Keep it safe and do not reuse it.")

    print("=" * 48 + "\n")


def main():
    print("=" * 48)
    print("  PASSWORD COMPLEXITY CHECKER")
    print("  Prodigy InfoTech Cybersecurity Internship")
    print("  Passwords are never stored or shared.")
    print("=" * 48)

    while True:
        password = getpass.getpass("\n  Enter a password to check (or press Enter to quit): ")

        if not password:
            print("\n  Goodbye!\n")
            break

        score, strength, suggestions, warnings = check_password(password)
        show_results(password, score, strength, suggestions, warnings)

        again = input("  Check another password? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
