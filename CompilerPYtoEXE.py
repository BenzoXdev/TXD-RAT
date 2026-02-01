# -*- coding: utf-8 -*-
# TXD - by benzoXdev
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Toplevel
from tkinter import ttk  # Import ttk for Progressbar
import threading
from PIL import Image, ImageTk
import os

def compile_to_exe():
    # Get Bot Token and Server ID
    bot_token = entry_token.get()
    server_id = entry_server.get()

    if not bot_token or not server_id:
        messagebox.showerror("Error", "Please enter both parameters: Bot Token and Server ID.")
        return

    # Open the Python file to edit
    file_path = filedialog.askopenfilename(
        defaultextension=".py",
        filetypes=[("Python Files", "*.py")],
        title="Select bot file"
    )

    if not file_path:
        return  # User cancelled

    # Create progress window
    progress_window = Toplevel()
    progress_window.title("TXD - Compiling...")
    progress_window.geometry("500x150")
    progress_window.configure(bg="#2E2E2E")
    progress_window.resizable(False, False)

    # Add logo image
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "logoCompiler", "diablo_emote.png")

        diablo_img = Image.open(image_path)
        diablo_img = diablo_img.resize((50, 50))
        diablo_photo = ImageTk.PhotoImage(diablo_img)
        
        label_diablo = tk.Label(progress_window, image=diablo_photo, bg="#2E2E2E")
        label_diablo.image = diablo_photo
        label_diablo.pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Error", "Could not find the logo image. Make sure the path is correct.")
        return
    
    # Create progress bar
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=400, mode="indeterminate")
    progress_bar.pack(pady=10)
    progress_bar.start()

    # Compilation function
    def compile_process():
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()

            # Replace bot_token and server_id
            file_content = file_content.replace('bot_token = "{bot_token}"', f'bot_token = "{bot_token}"')
            file_content = file_content.replace('server_id = "{server_id}"', f'server_id = "{server_id}"')

            # Save file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(file_content)

            # Select output folder
            output_directory = filedialog.askdirectory(title="Select destination folder for the executable")
            if not output_directory:
                raise ValueError("No destination folder selected.")

            #################################################################
            #           TXD - PyInstaller auto-detection                     #
            #################################################################

            # Use PyInstaller from PATH
            pyinstaller_path = shutil.which("pyinstaller") or shutil.which("pyinstaller.exe") or "pyinstaller"

            # Build command
            command = f'"{pyinstaller_path}" --onefile --noconsole --distpath "{output_directory}" "{file_path}"'

            # Run PyInstaller
            subprocess.run(command, shell=True, check=True)

            # Close progress window
            progress_window.destroy()
            messagebox.showinfo("TXD - Success", f"The .exe file was generated successfully in: {output_directory}")

        except Exception as e:
            progress_window.destroy()
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Run compilation in thread
    compile_thread = threading.Thread(target=compile_process)
    compile_thread.start()


# Create GUI
root = tk.Tk()
root.title("TXD - by benzoXdev")
root.geometry("500x400")
root.configure(bg="#2E2E2E")
root.resizable(False, False)

# Style
style_font = ("Arial", 14)
style_fg = "#00FF00"
style_bg = "#2E2E2E"
button_fg = "#FFFFFF"
button_bg = "#4CAF50"
button_hover = "#45a049"

# Title
label_title = tk.Label(root, text="TXD - by benzoXdev", font=("Arial", 20, "bold"), fg=style_fg, bg=style_bg)
label_title.pack(pady=20)

# Bot Token
label_token = tk.Label(root, text="Bot Token:", font=style_font, fg=style_fg, bg=style_bg)
label_token.pack(pady=10)

entry_token = tk.Entry(root, width=40, font=style_font, fg=style_fg, bg="#1C1C1C", insertbackground=style_fg, relief="flat", bd=0)
entry_token.pack(pady=10)

# Server ID
label_server = tk.Label(root, text="Server ID:", font=style_font, fg=style_fg, bg=style_bg)
label_server.pack(pady=10)

entry_server = tk.Entry(root, width=40, font=style_font, fg=style_fg, bg="#1C1C1C", insertbackground=style_fg, relief="flat", bd=0)
entry_server.pack(pady=10)

# Compile button
def on_hover(event):
    compile_button.config(bg=button_hover)

def on_leave(event):
    compile_button.config(bg=button_bg)

compile_button = tk.Button(root, text="Compile to .exe", font=("Arial", 16, "bold"), fg=button_fg, bg=button_bg, relief="flat", command=compile_to_exe)
compile_button.pack(pady=30)

# Hover effect
compile_button.bind("<Enter>", on_hover)
compile_button.bind("<Leave>", on_leave)

root.mainloop()
