import tkinter as tk
from PIL import Image, ImageTk
from header import Header
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PowermeterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header = Header(self, controller)
        header.grid(row=0, column=0, sticky="ew")

        image = Image.open("bg2.png")
        image = image.resize((800, 600), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        powerhead_text = "See the results"
        self.canvas.create_text(400, 100, text=powerhead_text, font=("Helvetica", 16), fill="black", justify="center", anchor="s")

        # Create a frame to display the power result
        self.result_frame = tk.Frame(self.canvas, bg="white", bd=2, relief="sunken")
        self.result_frame.place(x=300, y=200, width=200, height=100)
        self.power_label = tk.Label(self.result_frame, text="Power: ", font=("Helvetica", 14), bg="white")
        self.power_label.pack(pady=10)

        # Initialize the ADS1115 sensor
        self.sensor_connected = False
        try:
            self.i2c_bus = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS.ADS1115(self.i2c_bus)
            self.chan = AnalogIn(self.ads, ADS.P0)  # Reading from channel 0
            self.sensor_connected = True
        except ValueError as e:
            self.power_label.config(text="Error: ADS1115 not connected")
            print(f"Error initializing ADS1115: {e}")

        # Initialize plot data
        self.xdata, self.ydata = [], []

        # Buttons
        button_change_sensor = tk.Button(self, text="Change sensor", command=lambda: controller.show_frame("SensorsPage"), font=("Helvetica", 14), bg="white", fg="black", padx=16, pady=10)
        self.canvas.create_window(400, 400, anchor="s", window=button_change_sensor)

        button_show_dashboard = tk.Button(self, text="Show Dashboard", command=self.show_dashboard, font=("Helvetica", 14), bg="white", fg="black", padx=16, pady=10)
        self.canvas.create_window(400, 450, anchor="s", window=button_show_dashboard)

        footer_text = "© All rights reserved Sagemcom"
        self.canvas.create_text(400, 500, text=footer_text, font=("Helvetica", 16), fill="black", justify="center", anchor="s")

        # Update power reading
        self.update_power()

    def update_power(self):
        if self.sensor_connected:
            try:
                voltage = self.chan.voltage
                power = voltage * 1  # Simplified example, replace with actual calculation
                self.power_label.config(text=f"Power: {power:.2f} W")
                self.xdata.append(len(self.xdata))
                self.ydata.append(power)
            except Exception as e:
                self.power_label.config(text="Error reading power")
                print(f"Error: {e}")
        else:
            self.power_label.config(text="Error: ADS1115 not connected")
        self.after(1000, self.update_power)  # Update every 1 second

    def show_dashboard(self):
        # Update the plot page with the latest data
        self.controller.update_plot_page(self.xdata, self.ydata)
        # Switch to the plotting page
        self.controller.show_frame("PlotPage")

