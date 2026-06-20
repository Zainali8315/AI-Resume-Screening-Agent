# =============================================================================
# gui.py
# AI Resume Screening Agent — Full GUI (Tkinter / ttk)
# Screens: Home | Job Description | Add Candidates | Results | Shortlisted | About
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import screening_engine as engine
import data as sample_data

# ----------------------------------------------------------------------------
# COLOUR PALETTE & FONTS
# ----------------------------------------------------------------------------
BG_DARK      = "#1a1a2e"   # Deep navy – main background
BG_CARD      = "#16213e"   # Slightly lighter – card panels
BG_ACCENT    = "#0f3460"   # Blue accent – headers, sidebar
HIGHLIGHT    = "#e94560"   # Red-pink – primary buttons / accents
TEXT_LIGHT   = "#eaeaea"   # Near-white text
TEXT_MUTED   = "#a0a0c0"   # Muted purple-grey text
SUCCESS      = "#2ecc71"   # Green
WARNING      = "#f39c12"   # Orange
DANGER       = "#e74c3c"   # Red
INFO_BLUE    = "#3498db"   # Info blue

FONT_TITLE   = ("Segoe UI", 22, "bold")
FONT_HEAD    = ("Segoe UI", 14, "bold")
FONT_SUBHEAD = ("Segoe UI", 11, "bold")
FONT_BODY    = ("Segoe UI", 10)
FONT_SMALL   = ("Segoe UI", 9)
FONT_MONO    = ("Consolas", 9)


# ----------------------------------------------------------------------------
# HELPER: Styled Button
# ----------------------------------------------------------------------------
def styled_btn(parent, text, command, bg=HIGHLIGHT, fg="white",
               font=FONT_SUBHEAD, padx=18, pady=8, width=None):
    """Creates a consistently styled button."""
    kw = dict(text=text, command=command, bg=bg, fg=fg,
               font=font, relief="flat", cursor="hand2",
               padx=padx, pady=pady, bd=0, activebackground=bg,
               activeforeground=fg)
    if width:
        kw["width"] = width
    return tk.Button(parent, **kw)


def separator(parent, color=BG_ACCENT, height=2):
    """Thin coloured separator line."""
    return tk.Frame(parent, bg=color, height=height)


# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================
class ResumeScreenerApp(tk.Tk):
    """
    Main application window.
    Uses a frame-switching pattern — each 'screen' is a Frame raised to top.
    """

    def __init__(self):
        super().__init__()
        self.title("AI Resume Screening Agent")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # ── Application State ──────────────────────────────────────────────
        self.job_data        = {}          # Current job description dict
        self.candidates      = []          # List of candidate dicts
        self.results         = []          # Screening results (ranked)

        # ── Build layout ──────────────────────────────────────────────────
        self._build_nav()
        self._build_frames()
        self.show_frame("HomeScreen")

    # ─────────────────────────────────────────────────────────────────────
    # TOP NAVIGATION BAR
    # ─────────────────────────────────────────────────────────────────────
    def _build_nav(self):
        nav = tk.Frame(self, bg=BG_ACCENT, height=52)
        nav.pack(side="top", fill="x")
        nav.pack_propagate(False)

        # Logo / brand
        tk.Label(nav, text="🤖 AI Resume Screener",
                 bg=BG_ACCENT, fg=TEXT_LIGHT,
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=20, pady=10)

        # Navigation buttons
        nav_items = [
            ("🏠 Home",         "HomeScreen"),
            ("📋 Job Desc",     "JobScreen"),
            ("👤 Candidates",   "CandidateScreen"),
            ("📊 Results",      "ResultsScreen"),
            ("⭐ Shortlisted",  "ShortlistedScreen"),
            ("ℹ️ About",        "AboutScreen"),
        ]
        for label, frame_name in nav_items:
            btn = tk.Button(nav, text=label,
                            command=lambda fn=frame_name: self.show_frame(fn),
                            bg=BG_ACCENT, fg=TEXT_LIGHT,
                            font=FONT_SMALL, relief="flat",
                            cursor="hand2", padx=10, pady=14,
                            activebackground=HIGHLIGHT,
                            activeforeground="white")
            btn.pack(side="left")

    # ─────────────────────────────────────────────────────────────────────
    # BUILD ALL SCREEN FRAMES
    # ─────────────────────────────────────────────────────────────────────
    def _build_frames(self):
        """Create all screen frames stacked on top of each other."""
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True)

        self.frames = {}
        screen_classes = [
            HomeScreen,
            JobScreen,
            CandidateScreen,
            ResultsScreen,
            ShortlistedScreen,
            AboutScreen,
        ]
        for ScreenClass in screen_classes:
            frame = ScreenClass(container, self)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[ScreenClass.__name__] = frame

    def show_frame(self, name):
        """Raise the named frame to the top (switch screen)."""
        frame = self.frames[name]
        # Refresh dynamic screens before showing
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    # ─────────────────────────────────────────────────────────────────────
    # SCREENING TRIGGER
    # ─────────────────────────────────────────────────────────────────────
    def run_screening(self):
        """Run the AI screening engine and navigate to Results."""
        if not self.job_data:
            messagebox.showwarning("Missing Job", "Please fill in the Job Description first.")
            self.show_frame("JobScreen")
            return
        if not self.candidates:
            messagebox.showwarning("No Candidates", "Please add at least one candidate.")
            self.show_frame("CandidateScreen")
            return

        # ── Run AI Screening ──────────────────────────────────────────
        self.results = engine.screen_all(self.job_data, self.candidates)
        self.show_frame("ResultsScreen")


# ============================================================================
# SCREEN 1 — HOME
# ============================================================================
class HomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        # ── Hero section ──────────────────────────────────────────────
        hero = tk.Frame(self, bg=BG_ACCENT, pady=40)
        hero.pack(fill="x")

        tk.Label(hero, text="🤖", font=("Segoe UI", 48),
                 bg=BG_ACCENT, fg=HIGHLIGHT).pack()
        tk.Label(hero, text="AI Resume Screening Agent",
                 bg=BG_ACCENT, fg=TEXT_LIGHT, font=FONT_TITLE).pack(pady=(5, 2))
        tk.Label(hero,
                 text="Intelligent Candidate Ranking Powered by Expert Systems & AI",
                 bg=BG_ACCENT, fg=TEXT_MUTED, font=FONT_BODY).pack()

        separator(self, HIGHLIGHT, 3).pack(fill="x")

        # ── Description cards ─────────────────────────────────────────
        desc_frame = tk.Frame(self, bg=BG_DARK, pady=20)
        desc_frame.pack(fill="x", padx=60)

        cards_data = [
            ("📝", "Expert System",    "Rule-based AI decides each candidate's suitability"),
            ("📈", "Weighted Scoring", "Linear model scores Skills, Exp, Education, Keywords"),
            ("🏆", "Greedy Ranking",   "Greedily sorts all candidates: best match first"),
        ]
        for icon, title, desc in cards_data:
            card = tk.Frame(desc_frame, bg=BG_CARD, relief="flat",
                            padx=20, pady=15)
            card.pack(side="left", expand=True, fill="both", padx=10, pady=5)
            tk.Label(card, text=icon, font=("Segoe UI", 24),
                     bg=BG_CARD, fg=HIGHLIGHT).pack()
            tk.Label(card, text=title, font=FONT_SUBHEAD,
                     bg=BG_CARD, fg=TEXT_LIGHT).pack()
            tk.Label(card, text=desc, font=FONT_SMALL,
                     bg=BG_CARD, fg=TEXT_MUTED, wraplength=200).pack(pady=4)

        # ── Action Buttons ────────────────────────────────────────────
        btn_frame = tk.Frame(self, bg=BG_DARK, pady=30)
        btn_frame.pack()

        styled_btn(btn_frame, "▶  Start Screening",
                   command=self._start, bg=HIGHLIGHT, width=20).pack(side="left", padx=10)
        styled_btn(btn_frame, "👤  View Candidates",
                   command=lambda: self.app.show_frame("CandidateScreen"),
                   bg=BG_ACCENT, width=20).pack(side="left", padx=10)
        styled_btn(btn_frame, "ℹ️  About Project",
                   command=lambda: self.app.show_frame("AboutScreen"),
                   bg="#444466", width=20).pack(side="left", padx=10)

        # ── Footer ────────────────────────────────────────────────────
        separator(self, BG_ACCENT).pack(fill="x", side="bottom")
        tk.Label(self, text="Introduction to Artificial Intelligence Lab — Semester Project",
                 bg=BG_DARK, fg=TEXT_MUTED, font=FONT_SMALL).pack(side="bottom", pady=6)

    def _start(self):
        """Load sample data if none exists, then go to Job screen."""
        if not self.app.job_data:
            self.app.job_data = dict(sample_data.DEFAULT_JOB)
        if not self.app.candidates:
            self.app.candidates = [dict(c) for c in sample_data.SAMPLE_CANDIDATES]
            messagebox.showinfo("Demo Data Loaded",
                                f"Loaded {len(self.app.candidates)} sample candidates.\n"
                                "You can add/edit candidates on the Candidates screen.")
        self.app.show_frame("JobScreen")


# ============================================================================
# SCREEN 2 — JOB DESCRIPTION INPUT
# ============================================================================
class JobScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._entries = {}
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG_ACCENT, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📋  Job Description Input",
                 bg=BG_ACCENT, fg=TEXT_LIGHT, font=FONT_HEAD).pack(side="left", padx=20)

        # Card
        card = tk.Frame(self, bg=BG_CARD, padx=40, pady=30)
        card.pack(fill="both", expand=True, padx=40, pady=20)

        # Form fields
        fields = [
            ("job_title",   "💼 Job Title",                   "e.g. Software Engineer"),
            ("skills",      "🛠️  Required Skills (comma-sep)", "e.g. Python, Django, SQL"),
            ("experience",  "🕐 Required Experience (years)",  "e.g. 2"),
            ("education",   "🎓 Required Education",           "e.g. Bachelor in Computer Science"),
            ("keywords",    "🔑 Important Keywords (comma-sep)","e.g. agile, backend, api"),
        ]

        for key, label, placeholder in fields:
            row = tk.Frame(card, bg=BG_CARD)
            row.pack(fill="x", pady=8)

            tk.Label(row, text=label, font=FONT_SUBHEAD,
                     bg=BG_CARD, fg=TEXT_LIGHT, width=34, anchor="w").pack(side="left")

            if key == "keywords":
                # Multi-line for keywords
                entry = tk.Text(row, height=2, font=FONT_BODY,
                                bg=BG_DARK, fg=TEXT_LIGHT,
                                insertbackground=TEXT_LIGHT,
                                relief="flat", bd=6)
                entry.insert("1.0", placeholder)
                entry.config(fg=TEXT_MUTED)

                def _focus_in(e, w=entry, ph=placeholder):
                    if w.get("1.0", "end-1c") == ph:
                        w.delete("1.0", tk.END)
                        w.config(fg=TEXT_LIGHT)

                def _focus_out(e, w=entry, ph=placeholder):
                    if not w.get("1.0", "end-1c").strip():
                        w.insert("1.0", ph)
                        w.config(fg=TEXT_MUTED)

                entry.bind("<FocusIn>",  _focus_in)
                entry.bind("<FocusOut>", _focus_out)
            else:
                entry = tk.Entry(row, font=FONT_BODY, width=50,
                                 bg=BG_DARK, fg=TEXT_MUTED,
                                 insertbackground=TEXT_LIGHT,
                                 relief="flat", bd=6)
                entry.insert(0, placeholder)

                def _focus_in(e, w=entry, ph=placeholder):
                    if w.get() == ph:
                        w.delete(0, tk.END)
                        w.config(fg=TEXT_LIGHT)

                def _focus_out(e, w=entry, ph=placeholder):
                    if not w.get().strip():
                        w.insert(0, ph)
                        w.config(fg=TEXT_MUTED)

                entry.bind("<FocusIn>",  _focus_in)
                entry.bind("<FocusOut>", _focus_out)

            entry.pack(side="left", fill="x", expand=True)
            self._entries[key] = (entry, placeholder)

        separator(card, HIGHLIGHT, 1).pack(fill="x", pady=15)

        # Buttons row
        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack()

        styled_btn(btn_row, "💾  Save Job Description",
                   self._save_job, bg=SUCCESS).pack(side="left", padx=8)
        styled_btn(btn_row, "📂  Load Sample Job",
                   self._load_sample, bg=INFO_BLUE).pack(side="left", padx=8)
        styled_btn(btn_row, "🗑️  Clear",
                   self._clear, bg=DANGER).pack(side="left", padx=8)
        styled_btn(btn_row, "▶  Go to Candidates",
                   lambda: self.app.show_frame("CandidateScreen"),
                   bg=HIGHLIGHT).pack(side="left", padx=8)

    def _get_value(self, key):
        widget, placeholder = self._entries[key]
        if isinstance(widget, tk.Text):
            val = widget.get("1.0", "end-1c").strip()
            return "" if val == placeholder else val
        else:
            val = widget.get().strip()
            return "" if val == placeholder else val

    def _save_job(self):
        title = self._get_value("job_title")
        if not title:
            messagebox.showwarning("Input Error", "Please enter a Job Title.")
            return
        self.app.job_data = {
            "title":      title,
            "skills":     self._get_value("skills"),
            "experience": self._get_value("experience"),
            "education":  self._get_value("education"),
            "keywords":   self._get_value("keywords"),
        }
        messagebox.showinfo("Saved", f"Job description saved for:\n{title}")

    def _load_sample(self):
        """Populate fields with a sample job."""
        job = sample_data.DEFAULT_JOB
        placeholders = {
            "job_title":  "e.g. Software Engineer",
            "skills":     "e.g. Python, Django, SQL",
            "experience": "e.g. 2",
            "education":  "e.g. Bachelor in Computer Science",
            "keywords":   "e.g. agile, backend, api",
        }
        values = {
            "job_title":  job["title"],
            "skills":     job["skills"],
            "experience": job["experience"],
            "education":  job["education"],
            "keywords":   job["keywords"],
        }
        for key, val in values.items():
            widget, _ = self._entries[key]
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                widget.insert("1.0", val)
                widget.config(fg=TEXT_LIGHT)
            else:
                widget.delete(0, tk.END)
                widget.insert(0, val)
                widget.config(fg=TEXT_LIGHT)
        self.app.job_data = dict(job)
        messagebox.showinfo("Loaded", "Sample job description loaded!")

    def _clear(self):
        for key, (widget, placeholder) in self._entries.items():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                widget.insert("1.0", placeholder)
                widget.config(fg=TEXT_MUTED)
            else:
                widget.delete(0, tk.END)
                widget.insert(0, placeholder)
                widget.config(fg=TEXT_MUTED)
        self.app.job_data = {}


# ============================================================================
# SCREEN 3 — CANDIDATE ENTRY
# ============================================================================
class CandidateScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG_ACCENT, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="👤  Candidate Entry & Management",
                 bg=BG_ACCENT, fg=TEXT_LIGHT, font=FONT_HEAD).pack(side="left", padx=20)

        # Main layout: left = form, right = list
        main = tk.Frame(self, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # ── Left: Input Form ──────────────────────────────────────────
        form_card = tk.Frame(main, bg=BG_CARD, padx=20, pady=20)
        form_card.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(form_card, text="Add New Candidate",
                 bg=BG_CARD, fg=HIGHLIGHT, font=FONT_SUBHEAD).pack(anchor="w")
        separator(form_card, HIGHLIGHT, 1).pack(fill="x", pady=6)

        self._form_entries = {}
        simple_fields = [
            ("name",           "👤 Full Name",              "e.g. John Doe"),
            ("skills",         "🛠️  Skills (comma-sep)",    "e.g. Python, SQL, Git"),
            ("experience",     "🕐 Experience (years)",     "e.g. 3"),
            ("education",      "🎓 Education",              "e.g. Bachelor in CS"),
            ("certifications", "🏅 Certifications",        "e.g. AWS, Google Cloud"),
        ]
        for key, label, ph in simple_fields:
            f = tk.Frame(form_card, bg=BG_CARD)
            f.pack(fill="x", pady=4)
            tk.Label(f, text=label, font=FONT_SMALL,
                     bg=BG_CARD, fg=TEXT_MUTED, width=26, anchor="w").pack(side="left")
            entry = tk.Entry(f, font=FONT_BODY, bg=BG_DARK, fg=TEXT_MUTED,
                             insertbackground=TEXT_LIGHT, relief="flat", bd=4)
            entry.insert(0, ph)

            def _fi(e, w=entry, p=ph):
                if w.get() == p:
                    w.delete(0, tk.END); w.config(fg=TEXT_LIGHT)
            def _fo(e, w=entry, p=ph):
                if not w.get().strip():
                    w.insert(0, p); w.config(fg=TEXT_MUTED)

            entry.bind("<FocusIn>",  _fi)
            entry.bind("<FocusOut>", _fo)
            entry.pack(side="left", fill="x", expand=True)
            self._form_entries[key] = (entry, ph)

        # Resume text
        tk.Label(form_card, text="📄 Resume Summary",
                 bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", pady=(8, 2))
        self._resume_text = scrolledtext.ScrolledText(
            form_card, height=5, font=FONT_MONO,
            bg=BG_DARK, fg=TEXT_MUTED, insertbackground=TEXT_LIGHT,
            relief="flat", bd=4)
        self._resume_text.insert("1.0", "Paste or type candidate's resume summary here...")
        self._resume_text.pack(fill="x")

        btn_row = tk.Frame(form_card, bg=BG_CARD)
        btn_row.pack(pady=10)
        styled_btn(btn_row, "➕ Add Candidate", self._add_candidate,
                   bg=SUCCESS).pack(side="left", padx=5)
        styled_btn(btn_row, "📂 Load Samples",  self._load_samples,
                   bg=INFO_BLUE).pack(side="left", padx=5)
        styled_btn(btn_row, "🗑️ Clear Form",    self._clear_form,
                   bg=DANGER).pack(side="left", padx=5)

        # ── Right: Candidate List ─────────────────────────────────────
        list_card = tk.Frame(main, bg=BG_CARD, padx=15, pady=15)
        list_card.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tk.Label(list_card, text="Candidate List",
                 bg=BG_CARD, fg=HIGHLIGHT, font=FONT_SUBHEAD).pack(anchor="w")
        separator(list_card, HIGHLIGHT, 1).pack(fill="x", pady=6)

        # Candidate listbox
        self._listbox_var = tk.StringVar()
        self._listbox = tk.Listbox(list_card,
                                   listvariable=self._listbox_var,
                                   font=FONT_BODY, bg=BG_DARK,
                                   fg=TEXT_LIGHT, selectbackground=HIGHLIGHT,
                                   relief="flat", bd=0,
                                   activestyle="none")
        self._listbox.pack(fill="both", expand=True)

        list_btn_row = tk.Frame(list_card, bg=BG_CARD)
        list_btn_row.pack(pady=8)
        styled_btn(list_btn_row, "❌ Remove Selected",
                   self._remove_candidate, bg=DANGER).pack(side="left", padx=5)
        styled_btn(list_btn_row, "🧹 Clear All",
                   self._clear_all, bg="#555577").pack(side="left", padx=5)
        styled_btn(list_btn_row, "▶ Run Screening",
                   self.app.run_screening, bg=HIGHLIGHT).pack(side="left", padx=5)

        self._refresh_list()

    def _get_form_value(self, key):
        widget, ph = self._form_entries[key]
        val = widget.get().strip()
        return "" if val == ph else val

    def _add_candidate(self):
        name = self._get_form_value("name")
        if not name:
            messagebox.showwarning("Input Error", "Candidate name is required.")
            return

        resume = self._resume_text.get("1.0", "end-1c").strip()
        if resume == "Paste or type candidate's resume summary here...":
            resume = ""

        candidate = {
            "name":           name,
            "skills":         self._get_form_value("skills"),
            "experience":     self._get_form_value("experience"),
            "education":      self._get_form_value("education"),
            "certifications": self._get_form_value("certifications"),
            "resume_text":    resume,
        }
        self.app.candidates.append(candidate)
        self._refresh_list()
        self._clear_form()
        messagebox.showinfo("Added", f"Candidate '{name}' added successfully.")

    def _remove_candidate(self):
        sel = self._listbox.curselection()
        if not sel:
            messagebox.showinfo("Select Candidate", "Please select a candidate to remove.")
            return
        idx = sel[0]
        removed = self.app.candidates.pop(idx)
        self._refresh_list()
        messagebox.showinfo("Removed", f"Removed: {removed['name']}")

    def _clear_all(self):
        if messagebox.askyesno("Confirm", "Remove ALL candidates?"):
            self.app.candidates.clear()
            self._refresh_list()

    def _load_samples(self):
        self.app.candidates = [dict(c) for c in sample_data.SAMPLE_CANDIDATES]
        self._refresh_list()
        messagebox.showinfo("Loaded", f"{len(self.app.candidates)} sample candidates loaded.")

    def _clear_form(self):
        for key, (widget, ph) in self._form_entries.items():
            widget.delete(0, tk.END)
            widget.insert(0, ph)
            widget.config(fg=TEXT_MUTED)
        self._resume_text.delete("1.0", tk.END)
        self._resume_text.insert("1.0", "Paste or type candidate's resume summary here...")
        self._resume_text.config(fg=TEXT_MUTED)

    def _refresh_list(self):
        self._listbox.delete(0, tk.END)
        for i, c in enumerate(self.app.candidates, 1):
            self._listbox.insert(tk.END, f"  {i}. {c['name']}  ({c['experience']} yrs exp)")

    def on_show(self):
        self._refresh_list()


# ============================================================================
# SCREEN 4 — RESULTS
# ============================================================================
class ResultsScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._detail_window = None
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG_ACCENT, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📊  Screening Results — AI Ranked Candidates",
                 bg=BG_ACCENT, fg=TEXT_LIGHT, font=FONT_HEAD).pack(side="left", padx=20)

        styled_btn(hdr, "▶ Re-Screen", self.app.run_screening,
                   bg=HIGHLIGHT, pady=4).pack(side="right", padx=10)
        styled_btn(hdr, "⭐ View Shortlisted",
                   lambda: self.app.show_frame("ShortlistedScreen"),
                   bg=SUCCESS, pady=4).pack(side="right", padx=5)

        # Treeview table
        columns = ("rank", "name", "score", "skills", "exp", "edu", "kw", "status")
        col_labels = {
            "rank":   ("Rank",       50),
            "name":   ("Candidate",  160),
            "score":  ("Score %",    80),
            "skills": ("Skills %",   80),
            "exp":    ("Exp %",      70),
            "edu":    ("Edu %",      70),
            "kw":     ("Keywords %", 90),
            "status": ("Status",     160),
        }

        tree_frame = tk.Frame(self, bg=BG_DARK)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_CARD, fieldbackground=BG_CARD,
                        foreground=TEXT_LIGHT, font=FONT_BODY, rowheight=32)
        style.configure("Treeview.Heading",
                        background=BG_ACCENT, foreground=TEXT_LIGHT,
                        font=FONT_SUBHEAD)
        style.map("Treeview", background=[("selected", HIGHLIGHT)])

        self._tree = ttk.Treeview(tree_frame, columns=columns,
                                   show="headings", selectmode="browse")
        for col in columns:
            label, width = col_labels[col]
            self._tree.heading(col, text=label)
            self._tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                   command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._tree.bind("<Double-1>", self._show_detail)

        # Legend
        legend = tk.Frame(self, bg=BG_DARK)
        legend.pack(fill="x", padx=15, pady=4)
        tk.Label(legend, text="Double-click a candidate for details  |  Legend:",
                 bg=BG_DARK, fg=TEXT_MUTED, font=FONT_SMALL).pack(side="left")
        for status, color in [("Highly Recommended", "#1a7a1a"),
                               ("Recommended", "#2d862d"),
                               ("Average", "#cc8800"),
                               ("Not Recommended", "#cc2200")]:
            tk.Label(legend, text=f"  ● {status}", bg=BG_DARK,
                     fg=color, font=FONT_SMALL).pack(side="left")

    def on_show(self):
        """Refresh table with latest results."""
        self._tree.delete(*self._tree.get_children())
        for r in self.app.results:
            tag = r["status"].replace(" ", "_").lower()
            self._tree.insert("", tk.END, iid=str(r["rank"]), values=(
                f"#{r['rank']}",
                r["name"],
                f"{r['score']}%",
                f"{r['skill_pct']}%",
                f"{r['exp_pct']}%",
                f"{r['edu_pct']}%",
                f"{r['kw_pct']}%",
                r["status"],
            ), tags=(tag,))

        # Color rows by status
        self._tree.tag_configure("highly_recommended", foreground="#2ecc71")
        self._tree.tag_configure("recommended",        foreground="#27ae60")
        self._tree.tag_configure("average",            foreground="#f39c12")
        self._tree.tag_configure("not_recommended",    foreground="#e74c3c")

    def _show_detail(self, event):
        """Show a popup with full candidate analysis."""
        sel = self._tree.selection()
        if not sel:
            return
        rank = int(sel[0])
        result = next((r for r in self.app.results if r["rank"] == rank), None)
        if not result:
            return

        win = tk.Toplevel(self)
        win.title(f"Candidate Detail — {result['name']}")
        win.geometry("560x480")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)

        # Header
        hdr = tk.Frame(win, bg=BG_ACCENT, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"👤 {result['name']}",
                 bg=BG_ACCENT, fg=TEXT_LIGHT, font=FONT_HEAD).pack(side="left", padx=15)
        tk.Label(hdr, text=f"Rank #{result['rank']}",
                 bg=BG_ACCENT, fg=HIGHLIGHT, font=FONT_SUBHEAD).pack(side="right", padx=15)

        body = tk.Frame(win, bg=BG_DARK, padx=20, pady=15)
        body.pack(fill="both", expand=True)

        # Score big display
        score_frame = tk.Frame(body, bg=BG_CARD, pady=10)
        score_frame.pack(fill="x", pady=4)
        tk.Label(score_frame, text=f"Final Score: {result['score']}%",
                 bg=BG_CARD, fg=result['color'],
                 font=("Segoe UI", 18, "bold")).pack()
        tk.Label(score_frame, text=result['status'],
                 bg=BG_CARD, fg=result['color'],
                 font=FONT_SUBHEAD).pack()

        # Component scores
        comp_frame = tk.Frame(body, bg=BG_CARD, pady=8, padx=15)
        comp_frame.pack(fill="x", pady=6)
        tk.Label(comp_frame, text="Component Breakdown:",
                 bg=BG_CARD, fg=TEXT_LIGHT, font=FONT_SUBHEAD).pack(anchor="w")
        components = [
            ("Skills Match",    result['skill_pct'], 40),
            ("Experience",      result['exp_pct'],   25),
            ("Education",       result['edu_pct'],   15),
            ("Keywords",        result['kw_pct'],    15),
            ("Certifications",  result['cert_pct'],   5),
        ]
        for name, pct, weight in components:
            r = tk.Frame(comp_frame, bg=BG_CARD)
            r.pack(fill="x", pady=1)
            tk.Label(r, text=f"  {name} ({weight}%):",
                     bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL, width=24,
                     anchor="w").pack(side="left")
            tk.Label(r, text=f"{pct}%",
                     bg=BG_CARD, fg=(SUCCESS if pct >= 70 else WARNING if pct >= 40 else DANGER),
                     font=FONT_SMALL).pack(side="left")

        # Reasons
        tk.Label(body, text="AI Decision Reasons:",
                 bg=BG_DARK, fg=TEXT_LIGHT, font=FONT_SUBHEAD).pack(anchor="w", pady=(10, 2))
        reason_box = scrolledtext.ScrolledText(body, height=8, font=FONT_MONO,
                                               bg=BG_CARD, fg=TEXT_LIGHT,
                                               relief="flat", bd=4, wrap="word")
        reason_box.pack(fill="both", expand=True)
        for reason in result['reasons']:
            reason_box.insert(tk.END, f"{reason}\n")
        reason_box.config(state="disabled")

        styled_btn(win, "Close", win.destroy, bg=DANGER).pack(pady=10)


# ============================================================================
# SCREEN 5 — SHORTLISTED CANDIDATES
# ============================================================================
class ShortlistedScreen(tk.Frame):
    THRESHOLD = 70  # Minimum score to be shortlisted

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_ACCENT, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"⭐  Shortlisted Candidates (Score ≥ {self.THRESHOLD}%)",
                 bg=BG_ACCENT, fg=TEXT_LIGHT, font=FONT_HEAD).pack(side="left", padx=20)

        self._content = tk.Frame(self, bg=BG_DARK)
        self._content.pack(fill="both", expand=True, padx=20, pady=15)

    def on_show(self):
        for w in self._content.winfo_children():
            w.destroy()

        shortlisted = [r for r in self.app.results if r["score"] >= self.THRESHOLD]

        if not self.app.results:
            tk.Label(self._content,
                     text="No screening results yet.\nRun the screening first.",
                     bg=BG_DARK, fg=TEXT_MUTED, font=FONT_HEAD).pack(expand=True)
            return

        if not shortlisted:
            tk.Label(self._content,
                     text=f"No candidates scored ≥ {self.THRESHOLD}%.",
                     bg=BG_DARK, fg=WARNING, font=FONT_HEAD).pack(expand=True)
            return

        tk.Label(self._content,
                 text=f"✅ {len(shortlisted)} candidate(s) meet the threshold of {self.THRESHOLD}%",
                 bg=BG_DARK, fg=SUCCESS, font=FONT_SUBHEAD).pack(anchor="w", pady=(0, 10))

        scroll_canvas = tk.Canvas(self._content, bg=BG_DARK, highlightthickness=0)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(self._content, orient="vertical", command=scroll_canvas.yview)
        sb.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=sb.set)

        inner = tk.Frame(scroll_canvas, bg=BG_DARK)
        scroll_canvas.create_window((0, 0), window=inner, anchor="nw")

        for r in shortlisted:
            card = tk.Frame(inner, bg=BG_CARD, pady=12, padx=20,
                            relief="flat", bd=0)
            card.pack(fill="x", pady=5)

            top_row = tk.Frame(card, bg=BG_CARD)
            top_row.pack(fill="x")

            tk.Label(top_row, text=f"#{r['rank']}  {r['name']}",
                     bg=BG_CARD, fg=TEXT_LIGHT, font=FONT_SUBHEAD).pack(side="left")
            tk.Label(top_row, text=f"{r['score']}%  ●  {r['status']}",
                     bg=BG_CARD, fg=r['color'], font=FONT_SUBHEAD).pack(side="right")

            # Score bar
            bar_bg = tk.Frame(card, bg=BG_DARK, height=10)
            bar_bg.pack(fill="x", pady=4)
            bar_fill_width = int(r['score'])
            bar_fill = tk.Frame(bar_bg, bg=r['color'], height=10)
            bar_fill.place(relx=0, rely=0, relwidth=r['score']/100, relheight=1)

            summary = tk.Label(card, text="  |  ".join(r['reasons'][:2]),
                               bg=BG_CARD, fg=TEXT_MUTED, font=FONT_SMALL,
                               wraplength=800, justify="left")
            summary.pack(anchor="w")

        inner.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))


# ============================================================================
# SCREEN 6 — ABOUT
# ============================================================================
class AboutScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_ACCENT, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="ℹ️  About This Project",
                 bg=BG_ACCENT, fg=TEXT_LIGHT, font=FONT_HEAD).pack(side="left", padx=20)

        text_frame = tk.Frame(self, bg=BG_DARK, padx=30, pady=20)
        text_frame.pack(fill="both", expand=True)

        about_text = """
🎯  PROJECT OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This AI Resume Screening Agent automates the process of evaluating and ranking
job candidates. HR teams can define job requirements, add candidate profiles,
and receive instant AI-driven shortlists with full explanations.

🧠  AI TECHNIQUES USED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. EXPERT SYSTEM (Lab 14 — Rule-Based AI)
   Rule-based decision making with IF-THEN logic:
   • IF required skill found → increase score
   • IF experience ≥ required → full experience score
   • IF degree matches → full education score
   • IF keywords missing → penalty applied

2. WEIGHTED SCORING / LINEAR REGRESSION MODEL (Lab 12)
   Final Score = Skills×40% + Experience×25% + Education×15%
               + Keywords×15% + Certifications×5%
   Weights are fixed coefficients (like a trained linear model).

3. GREEDY RANKING ALGORITHM (Lab 06 / Lab 07)
   Candidates are ranked using a greedy sort:
   "Always pick the highest-scoring candidate next."
   This is O(n log n) and guarantees optimal ordering.

4. SEARCH ALGORITHM INSPIRATION (Lab 03 / Lab 04)
   File/candidate search resembles BFS/DFS traversal.
   Each candidate is a node; screening explores all nodes.

5. HILL CLIMBING CONCEPT (Lab 09)
   Score improvement = climbing the hill of suitability.
   Adding certifications or skills raises the score.

6. GENETIC ALGORITHM (Future Enhancement — Lab 10)
   Weight optimization could be automated via GA.

📚  SYLLABUS MAPPING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lab 01 → Python basics used throughout
Lab 02 → Candidate data stored in Python dicts/lists
Lab 06 → Greedy ranking by score
Lab 07 → Greedy selection (always pick best candidate)
Lab 09 → Score = hill-climbing analogy
Lab 10 → GA mentioned as future weight optimiser
Lab 12 → Weighted scoring model (linear regression-inspired)
Lab 14 → Expert system rules for decision making

🛠️  TECHNOLOGY STACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Language  : Python 3.x
• GUI       : Tkinter + ttk (built-in, no installation needed)
• AI Logic  : Custom screening_engine.py
• Data      : data.py (sample candidates and jobs)
• No APIs   : Runs 100% offline on any laptop
"""
        text_widget = scrolledtext.ScrolledText(
            text_frame, font=FONT_MONO,
            bg=BG_CARD, fg=TEXT_LIGHT,
            relief="flat", bd=6, wrap="word")
        text_widget.insert("1.0", about_text)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
