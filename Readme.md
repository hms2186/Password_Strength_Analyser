# Password Strength Analyzer & Custom Wordlist Generator

**Purpose:** Defensive tool to analyze password strength and generate custom wordlists for authorized security testing and password-hardening exercises.

**IMPORTANT:** Use only on passwords/accounts you own or have explicit permission to test. Misuse is illegal and unethical.

## Features
- Password strength evaluation using `zxcvbn` + entropy estimate.
- Custom wordlist generation from inputs (names, dates, pets, nicknames, extra words).
- Mutations: case variants, leetspeak, common suffixes, append recent years, combine tokens.
- Export to `.txt` (suitable for offline inspection or authorized testing).
- CLI and simple Tkinter GUI.

## Installation
1. Clone or copy project files.
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
