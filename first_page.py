import tkinter as tk
from PIL import Image, ImageTk
from header import Header

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        header = Header(self, controller)
        header.grid(row=0, column=0, sticky="ew")
        
        image = Image.open("bg2.png")
        image = image.resize((800, 600), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)
        
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        centered_text = "This application allows the user to test multiple \n type of sensors such as a voltmeter , powermeter \n and an LCD ."
        self.canvas.create_text(400, 100, text=centered_text, font=("Helvetica", 16), fill="black", justify="center", anchor="center")

        footer_text = "© All rights reserved Sagemcom"
        self.canvas.create_text(400, 500, text=footer_text, font=("Helvetica", 16), fill="black", justify="center", anchor="s")