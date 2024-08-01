import tkinter as tk
from PIL import Image, ImageTk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        image = Image.open("bg.png")
        image = image.resize((800, 600), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)
        
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        Welcome_text = "Welcome to Raspberrypi app"
        self.canvas.create_text(400, 100, text=Welcome_text, font=("Helvetica", 16), fill="black", justify="center", anchor="n")
        
        button = tk.Button(self, text="Enter", command=lambda: controller.show_frame("FirstPage"), font=("Helvetica", 14), bg="white", fg="black", padx=16, pady=10)
        self.canvas.create_window(400, 550, anchor="s", window=button)