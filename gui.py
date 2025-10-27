"""
gui.py
Simple Tkinter GUI for the tool.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from password_analyzer import analyze
from wordlist_generator import generate_wordlist, save_wordlist

class PWToolGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Analyzer & Wordlist Generator (Defensive Use Only)")
        self.geometry("700x520")
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        # Analyzer section
        ttk.Label(frm, text="Password Analyzer", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0,5))
        self.pw_entry = ttk.Entry(frm, width=50, show="*")
        self.pw_entry.pack(anchor=tk.W)
        ttk.Label(frm, text="Optional user inputs (comma-separated):").pack(anchor=tk.W, pady=(5,0))
        self.user_entry = ttk.Entry(frm, width=80)
        self.user_entry.pack(anchor=tk.W)
        ttk.Button(frm, text="Analyze", command=self.analyze_password).pack(anchor=tk.W, pady=(5,10))
        self.analysis_text = tk.Text(frm, height=8, wrap=tk.WORD)
        self.analysis_text.pack(fill=tk.BOTH, expand=False, pady=(0,10))

        # Generator section
        ttk.Label(frm, text="Custom Wordlist Generator", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(10,5))
        ttk.Label(frm, text="Base tokens (comma-separated, required):").pack(anchor=tk.W)
        self.base_entry = ttk.Entry(frm, width=80)
        self.base_entry.pack(anchor=tk.W)
        ttk.Label(frm, text="Extra tokens (comma-separated, optional):").pack(anchor=tk.W)
        self.extra_entry = ttk.Entry(frm, width=80)
        self.extra_entry.pack(anchor=tk.W)
        row = ttk.Frame(frm)
        row.pack(fill=tk.X, pady=(5,0))
        ttk.Label(row, text="Years from:").pack(side=tk.LEFT)
        self.year_from = ttk.Entry(row, width=6); self.year_from.pack(side=tk.LEFT, padx=(5,10))
        ttk.Label(row, text="to:").pack(side=tk.LEFT)
        self.year_to = ttk.Entry(row, width=6); self.year_to.pack(side=tk.LEFT, padx=(5,10))
        self.year_from.insert(0, "2000")
        self.year_to.insert(0, "2026")
        ttk.Label(row, text="Max combine:").pack(side=tk.LEFT, padx=(10,0))
        self.max_combine = ttk.Entry(row, width=3); self.max_combine.pack(side=tk.LEFT, padx=(5,10))
        self.max_combine.insert(0, "2")
        ttk.Label(row, text="Max total:").pack(side=tk.LEFT)
        self.max_total = ttk.Entry(row, width=6); self.max_total.pack(side=tk.LEFT, padx=(5,10))
        self.max_total.insert(0, "50000")
        self.leet_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frm, text="Include leet variants", variable=self.leet_var).pack(anchor=tk.W, pady=(5,0))
        ttk.Button(frm, text="Generate and Save", command=self.generate_save).pack(anchor=tk.W, pady=(10,0))
        self.generator_text = tk.Text(frm, height=10, wrap=tk.WORD)
        self.generator_text.pack(fill=tk.BOTH, expand=True, pady=(5,0))

    def analyze_password(self):
        pw = self.pw_entry.get().strip()
        users = [u.strip() for u in self.user_entry.get().split(",") if u.strip()]
        if not pw:
            messagebox.showwarning("Input required", "Enter a password to analyze.")
            return
        res = analyze(pw, user_inputs=users)
        out = []
        out.append(f"Score: {res['score']} ({res['strength_text']})")
        out.append(f"Estimated entropy: {res['estimated_entropy']:.2f} bits")
        feedback = res.get('feedback', {})
        if feedback.get('warning'):
            out.append("Warning: " + feedback['warning'])
        if feedback.get('suggestions'):
            out.append("Suggestions:")
            for s in feedback['suggestions']:
                out.append("  - " + s)
        if 'crack_times_display' in res:
            out.append("Crack times (display):")
            for k, v in res['crack_times_display'].items():
                out.append(f"  {k}: {v}")
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "\n".join(out))

    def generate_save(self):
        base = [b.strip() for b in self.base_entry.get().split(",") if b.strip()]
        extra = [e.strip() for e in self.extra_entry.get().split(",") if e.strip()]
        if not base:
            messagebox.showwarning("Input required", "Enter at least one base token.")
            return
        try:
            yf = int(self.year_from.get()); yt = int(self.year_to.get())
            mc = int(self.max_combine.get()); mt = int(self.max_total.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Year and numeric fields must be integers.")
            return
        wl = generate_wordlist(base, extra_tokens=extra, include_leet=self.leet_var.get(), include_years=(yf, yt), max_combination=mc, max_total=mt)
        # show sample
        self.generator_text.delete(1.0, tk.END)
        self.generator_text.insert(tk.END, f"Generated {len(wl)} entries. Showing first 200 lines:\n\n")
        for i, w in enumerate(wl[:200], 1):
            self.generator_text.insert(tk.END, f"{i:4d}: {w}\n")
        # ask to save
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save wordlist as")
        if save_path:
            save_wordlist(wl, save_path)
            messagebox.showinfo("Saved", f"Saved {len(wl)} words to {save_path}")

if __name__ == "__main__":
    app = PWToolGUI()
    app.mainloop()
