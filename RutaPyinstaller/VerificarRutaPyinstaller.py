# TXD - by benzoXdev
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import pyperclip
import re

# Function to run PyInstaller and get absolute path
def run_pyinstaller():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        process = subprocess.Popen(
            ['pyinstaller', '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=script_dir
        )

        stdout, stderr = process.communicate()

        if process.returncode == 0:
            absolute_path = os.path.abspath(script_dir)
            show_window(f"PyInstaller is working correctly.\n\nYou can use pyinstaller from this directory:\n{absolute_path}", absolute_path)
        else:
            error_message = stderr.decode("utf-8")
            match = re.search(r"(C:\\[^\\]+\\Scripts\\pyinstaller\.py)", error_message)
            if match:
                error_path = match.group(1)
                show_window(f"PyInstaller error. The pyinstaller.py file might be at:\n{error_path}", error_path)
            else:
                show_window(f"PyInstaller error:\n{error_message}", None)

    except Exception as e:
        messagebox.showerror("Error", f"Error executing PyInstaller:\n{str(e)}")

# Function to show window with path and copy option
def show_window(message, path):
    # Create main window
    window = tk.Tk()
    window.title("TXD - Verify PyInstaller - by benzoXdev")
    window.geometry("700x450")
    window.config(bg="#1a1a1a")
    
    # Title
    title_label = tk.Label(
        window,
        text="TXD - PyInstaller Status",
        font=("Courier New", 18, "bold"),
        bg="#1a1a1a",
        fg="#33ff33",
        pady=10
    )
    title_label.pack(pady=10)
    
    # Message label
    message_label = tk.Label(
        window,
        text=message,
        font=("Courier New", 12),
        bg="#1a1a1a",
        fg="#d1d1d1",
        justify="left",
        padx=20,
        pady=10
    )
    message_label.pack(pady=10)
    
    # Copy to clipboard button
    if path:
        def copy_to_clipboard():
            pyperclip.copy(path)
            messagebox.showinfo("Copied", "Path has been copied to clipboard.")
        
        copy_button = tk.Button(
            window,
            text="Copy to Clipboard",
            font=("Courier New", 12),
            command=copy_to_clipboard,
            bg="#4CAF50",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            bd=0,
            activebackground="#388E3C",
            activeforeground="white"
        )
        copy_button.pack(pady=20)
    
    # Exit button
    exit_button = tk.Button(
        window,
        text="Exit",
        font=("Courier New", 12),
        command=window.quit,
        bg="#ff3333",
        fg="white",
        relief="flat",
        padx=20,
        pady=10,
        bd=0,
        activebackground="#D32F2F",
        activeforeground="white"
    )
    exit_button.pack(pady=10)
    
    window.lift()
    window.attributes("-topmost", True)
    window.after(100, lambda: window.attributes("-topmost", False))

    window.mainloop()

# Run script
if __name__ == "__main__":
    run_pyinstaller()
