import tkinter as tk
from PIL import Image, ImageTk
from header import Header

class SensorsPage(tk.Frame):
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

        select_text = "Select sensor "
        self.canvas.create_text(400, 100, text=select_text, font=("Helvetica", 16), fill="black", justify="center", anchor="center")

        button_powermeter = tk.Button(self.canvas, text="Powermeter", command=lambda: controller.show_frame("PowermeterPage"), font=("Helvetica", 14), bg="white", fg="black")
        self.canvas.create_window(300, 250, anchor="center", window=button_powermeter)
        
        button_voltmeter = tk.Button(self.canvas, text="Voltmeter", command=lambda: controller.show_frame("VoltmeterPage"), font=("Helvetica", 14), bg="white", fg="black")
        self.canvas.create_window(500, 250, anchor="center", window=button_voltmeter)

        footer_text = "© All rights reserved Sagemcom"
        self.canvas.create_text(400, 500, text=footer_text, font=("Helvetica", 16), fill="black", justify="center", anchor="s")