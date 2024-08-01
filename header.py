import tkinter as tk

class Header(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        button_home = tk.Button(self, text="Home", command=lambda: controller.show_frame("FirstPage"))
        button_sensors = tk.Button(self, text="Sensors", command=lambda: controller.show_frame("SensorsPage"))
        button_lcd = tk.Button(self, text="LCD", command=lambda: controller.show_frame("LCDPage"))
        button_exit = tk.Button(self, text="Exit", command=lambda: controller.show_frame("HomePage"))
        
        button_home.grid(row=0, column=0, padx=10, pady=5)
        button_sensors.grid(row=0, column=1, padx=10, pady=5)
        button_lcd.grid(row=0, column=2, padx=10, pady=5)
        button_exit.grid(row=0, column=3, padx=10, pady=5)