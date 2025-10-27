 🔐 PWTool – Intelligent Password Strength Analyzer & Wordlist Generator


🧩 Overview
PWTool is a desktop-based Python application that evaluates password strength and generates custom wordlists for auditing weak credentials.
It uses the powerful zxcvbn algorithm (developed by Dropbox) to estimate password entropy and provide meaningful feedback.
The tool features a simple Tkinter GUI, along with CLI compatibility, making it useful for both everyday users and developers interested in studying password security.


🚀 Features
✅ Password Strength Analyzer
Evaluates passwords using the zxcvbn library.
Provides real-time feedback and strength scores.
Displays estimated crack time and detailed suggestions.
✅ Custom Wordlist Generator
Generates personalized wordlists based on user inputs (names, dates, patterns, etc.).
Can be used for password audits or penetration testing environments.
✅ GUI + CLI Support
User-friendly graphical interface (built with Tkinter).
Command-line compatibility for automation or scripting.
✅ Offline & Lightweight
Works completely offline after installation.
Single-file executable can be generated with PyInstaller.



🏗️ Project Architecture
+-------------------------+
|        GUI (Tkinter)    |
+-----------+-------------+
            |
            v
+-------------------------+
|   Password Analyzer     | --> Uses zxcvbn for strength metrics
+-----------+-------------+
            |
            v
+-------------------------+
|   Wordlist Generator    | --> Creates personalized lists
+-----------+-------------+
            |
            v
+-------------------------+
|     (Optional) DB       | --> Can store analysis logs or patterns
+-------------------------+

🖥️ Installation & Setup
Option 1 — Run with Python
Make sure you have Python 3.12+ installed.

# Clone or download this repository
cd PasswordTool

# (Optional but recommended) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Then run the GUI:
python3 gui.py

Option 2 — Run the Single Executable
If you built the standalone app using PyInstaller:
pyinstaller --onefile --windowed --name PWTool \
  --hidden-import=zxcvbn --hidden-import=zxcvbn._zxcvbn gui.py
You’ll find the .app (macOS) or .exe (Windows) file inside the dist/ folder.
Double-click it to launch the tool — no installation needed!


⚙️ Usage Guide:

🔹 Password Strength Analysis
Launch the GUI.
Enter a password in the input field.
Click Analyze Password.
The tool displays:
Strength score (0–4)
Estimated crack time
Suggestions for improvement

🔹 Generate a Custom Wordlist
Enter related words (names, dates, pet names, etc.)
Set desired pattern or length.
Click Generate Wordlist.
The tool saves the generated list in the local directory.


🧠 Technologies Used
Python 3.12+
Tkinter (GUI)
zxcvbn (Password strength analysis)
PyInstaller (Packaging)
SQLite3 / Optional DB module


🧾 References
Dropbox zxcvbn Documentation
Python Tkinter Documentation
PEP 668 – Externally Managed Environments


💬 Author & Acknowledgment
Developed by Hemanth
Thanks to the open-source Python and security community.


🛠️ Future Enhancements
Export analysis reports as PDF or CSV.
Add color-coded password meters.
Integrate online breach database checks.
Multi-user database tracking of password improvements.
