# TXD - by benzoXdev
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class GuiaCompresionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TXD - Self-Extracting Guide - by benzoXdev")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        # Variables for current step and images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, "buildEXE", "images")
        self.current_step = 1
        self.images = [
            os.path.join(images_dir, "paso1.png"),  # Step 1
            os.path.join(images_dir, "paso2.png"),  # Step 2
            os.path.join(images_dir, "paso3.png"),  # Step 3
            os.path.join(images_dir, "paso4.png"),  # Step 4
            os.path.join(images_dir, "paso5.png"),  # Step 5
            os.path.join(images_dir, "paso6.png"),  # Step 6
            os.path.join(images_dir, "paso7.png")   # Step 7
        ]

        self.instructions = [
            "Step 1: Add to archive... and select 'Create self-extracting archive'.",
            "Step 2: Go to the Advanced tab and check the self-extracting option.",
            "Step 3: In the Installation tab, in the 'Run after extraction' field.\n"
            "Add the names of the 2 selected files 'file1.vbs' and 'file2.exe'",
            "Step 4: In the Modes tab, select 'Extract to temporary folder'\n"
            "And select 'Hide startup dialog'",
            "Step 5: In the 'Text and icon' tab, select 'Load icon from file'.\n"
            "Choose the icon you want for your self-extracting file.",
            "Step 6: In the Update section, check 'Extract and update files'.\n"
            "Then select 'Overwrite all files'.",
            "Step 7: Return to the Advanced tab and select\n"
            "'Request administrator access'."
        ]

        self.create_widgets()

    def create_widgets(self):
        """ Create window widgets """
        # Label for current step instruction
        self.instruction_label = tk.Label(self.root, text=self.instructions[self.current_step - 1],
                                          font=("Consolas", 14), fg="#00FF00", bg="#1e1e1e", justify=tk.LEFT)
        self.instruction_label.pack(pady=20, padx=20)

        # Image for visual step
        self.step_image = self.load_image(self.images[self.current_step - 1])
        self.image_label = tk.Label(self.root, image=self.step_image, bd=0, relief="flat")
        self.image_label.pack(pady=20)

        # Navigation buttons
        self.back_button = tk.Button(self.root, text="<< Back", command=self.previous_step, state=tk.DISABLED,
                                     font=("Arial", 12), fg="#FFFFFF", bg="#333333", relief="flat", width=10)
        self.back_button.pack(side=tk.LEFT, padx=40)

        self.next_button = tk.Button(self.root, text="Next >>", command=self.next_step,
                                         font=("Arial", 12), fg="#FFFFFF", bg="#00FF00", relief="flat", width=12)
        self.next_button.pack(side=tk.RIGHT, padx=40)

        # Hover effects
        self.back_button.bind("<Enter>", self.on_hover_back)
        self.back_button.bind("<Leave>", self.on_leave_back)
        self.next_button.bind("<Enter>", self.on_hover_next)
        self.next_button.bind("<Leave>", self.on_leave_next)

    def load_image(self, path):
        """ Load and resize image """
        try:
            image = Image.open(path)
            image = image.resize((400, 450), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image {path}: {e}")
            return None

    def next_step(self):
        """ Go to next step """
        if self.current_step < len(self.instructions):
            self.current_step += 1
            self.update_step()

    def previous_step(self):
        """ Go to previous step """
        if self.current_step > 1:
            self.current_step -= 1
            self.update_step()

    def update_step(self):
        """ Update instruction and image for current step """
        # Update instructions
        self.instruction_label.config(text=self.instructions[self.current_step - 1])

        # Update image
        self.step_image = self.load_image(self.images[self.current_step - 1])
        self.image_label.config(image=self.step_image)

        # Enable or disable buttons
        if self.current_step == 1:
            self.back_button.config(state=tk.DISABLED)
        else:
            self.back_button.config(state=tk.NORMAL)

        if self.current_step == len(self.instructions):
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    def on_hover_back(self, event):
        """ Hover effect for Back button """
        self.back_button.config(bg="#444444")

    def on_leave_back(self, event):
        """ Restore Back button color """
        self.back_button.config(bg="#333333")

    def on_hover_next(self, event):
        """ Hover effect for Next button """
        self.next_button.config(bg="#00CC00")

    def on_leave_next(self, event):
        """ Restore Next button color """
        self.next_button.config(bg="#00FF00")


# Create main window
root = tk.Tk()

# Create application
app = GuiaCompresionApp(root)

# Run application
root.mainloop()
