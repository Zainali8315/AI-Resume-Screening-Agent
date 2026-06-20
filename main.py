# =============================================================================
# main.py
# AI Resume Screening Agent — Entry Point
# Run this file to launch the application.
#
# Usage:
#   python main.py
#
# Requirements:
#   Python 3.x (Tkinter is built-in — no extra installation needed)
# =============================================================================

import sys

def check_python_version():
    """Ensure Python 3 is being used."""
    if sys.version_info.major < 3:
        print("ERROR: This project requires Python 3.x")
        print(f"       You are using Python {sys.version}")
        sys.exit(1)

def main():
    check_python_version()

    # Import the GUI application
    from gui import ResumeScreenerApp

    print("=" * 55)
    print("   AI Resume Screening Agent")
    print("   Introduction to Artificial Intelligence Lab")
    print("   Semester Project")
    print("=" * 55)
    print("  Starting GUI...")

    # Create and run the application
    app = ResumeScreenerApp()

    # Center the window on screen
    app.update_idletasks()
    w = app.winfo_width()
    h = app.winfo_height()
    x = (app.winfo_screenwidth()  // 2) - (w // 2)
    y = (app.winfo_screenheight() // 2) - (h // 2)
    app.geometry(f"+{x}+{y}")

    print("  GUI launched successfully.")
    print("  Close the window to exit.")
    print("=" * 55)

    # Start the Tkinter event loop
    app.mainloop()

    print("  Application closed. Goodbye!")


if __name__ == "__main__":
    main()
