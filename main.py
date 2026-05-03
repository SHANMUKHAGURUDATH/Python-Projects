# -*- coding: utf-8 -*-

# Import required modules
import tkinter as tk                 # For GUI
from tkinter import filedialog      # For file open/save dialog
import subprocess                   # To run Python code
import sys                          # To get Python interpreter path
import os                           # For file handling


# Create main class
class PythonIDE:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("Python Mini IDE")      # Window title
        self.root.geometry("900x600")           # Window size
        self.root.configure(bg="#1e1e2e")       # Background color

        self.filename = None                    # To store file path

        # ---------------- TOP BAR ----------------
        top = tk.Frame(root, bg="#2d2d44")      # Top bar frame
        top.pack(fill="x")

        # Run button
        tk.Button(top, text="Run ▶", command=self.run_code,
                  bg="#5e5ce6", fg="white").pack(side="left", padx=5, pady=5)

        # Open file button
        tk.Button(top, text="Open", command=self.open_file).pack(side="left", padx=5)

        # Save file button
        tk.Button(top, text="Save", command=self.save_file).pack(side="left", padx=5)

        # Clear output button
        tk.Button(top, text="Clear Output", command=self.clear_output).pack(side="left", padx=5)

        # ---------------- CODE EDITOR ----------------
        self.text = tk.Text(root,
                            font=("Consolas", 13),
                            bg="#1e1e2e",
                            fg="white",
                            insertbackground="white")   # Cursor color
        self.text.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------------- OUTPUT CONSOLE ----------------
        self.output = tk.Text(root,
                              height=10,
                              bg="black",
                              fg="lime",
                              font=("Consolas", 11))
        self.output.pack(fill="x")

    # ---------------- OPEN FILE ----------------
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if file_path:
            self.filename = file_path
            with open(file_path, "r", encoding="utf-8") as f:
                self.text.delete(1.0, tk.END)      # Clear editor
                self.text.insert(tk.END, f.read()) # Load file content

    # ---------------- SAVE FILE ----------------
    def save_file(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".py")

        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(self.text.get(1.0, tk.END))  # Save code

    # ---------------- RUN CODE ----------------
    def run_code(self):
        code = self.text.get(1.0, tk.END)   # Get code from editor

        os.makedirs("temp", exist_ok=True)  # Create temp folder

        file_path = "temp/temp.py"          # Temp file path

        try:
            # Write code to temp file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Run Python file
            result = subprocess.run(
                [sys.executable, file_path],   # Use system Python
                capture_output=True,           # Capture output
                text=True,                    # Return text output
                encoding="utf-8"
            )

            # Show output and errors
            self.show_output(result.stdout + result.stderr)

        except Exception as e:
            self.show_output(str(e))          # Show error if occurs

    # ---------------- SHOW OUTPUT ----------------
    def show_output(self, text):
        self.output.delete(1.0, tk.END)      # Clear previous output
        self.output.insert(tk.END, text)     # Display new output

    # ---------------- CLEAR OUTPUT ----------------
    def clear_output(self):
        self.output.delete(1.0, tk.END)      # Clear console


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    root = tk.Tk()           # Create main window
    app = PythonIDE(root)    # Create app object
    root.mainloop()          # Run GUI loop
