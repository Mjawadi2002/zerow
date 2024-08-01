import tkinter as tk
from PIL import Image, ImageTk
from header import Header
import board
import busio
from adafruit_ina219 import INA219
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

class VoltmeterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.voltage_readings = []
        self.time_stamps = []
        self.start_time = time.time()
        
        header = Header(self, controller)
        header.grid(row=0, column=0, sticky="ew")
        
        image = Image.open("bg2.png")
        image = image.resize((800, 600), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)
        
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        
        volthead_text = "See the results"
        self.canvas.create_text(400, 100, text=volthead_text, font=("Helvetica", 16), fill="black", justify="center", anchor="s")

        # Create a frame to display the voltage result
        self.result_frame = tk.Frame(self.canvas, bg="white", bd=2, relief="sunken")
        self.result_frame.place(x=300, y=200, width=200, height=100)
        self.voltage_label = tk.Label(self.result_frame, text="Voltage: ", font=("Helvetica", 14), bg="white")
        self.voltage_label.pack(pady=10)
        
        # Initialize the INA219 sensor
        self.sensor_connected = False
        try:
            self.i2c_bus = busio.I2C(board.SCL, board.SDA)
            self.ina219 = INA219(self.i2c_bus)
            self.sensor_connected = True
        except ValueError as e:
            self.voltage_label.config(text="Error: INA219 not connected")
            print(f"Error initializing INA219: {e}")
        
        # Update voltage reading
        self.update_voltage()

        button_change_sensor = tk.Button(self, text="Change sensor", command=lambda: controller.show_frame("SensorsPage"), font=("Helvetica", 14), bg="white", fg="black", padx=16, pady=10)
        self.canvas.create_window(400, 400, anchor="s", window=button_change_sensor)

        button_see_dashboard = tk.Button(self, text="See Dashboard", command=self.show_dashboard, font=("Helvetica", 14), bg="white", fg="black", padx=16, pady=10)
        self.canvas.create_window(400, 450, anchor="s", window=button_see_dashboard)
        
        footer_text = "© All rights reserved Sagemcom"
        self.canvas.create_text(400, 500, text=footer_text, font=("Helvetica", 16), fill="black", justify="center", anchor="s")
    
    def update_voltage(self):
        if self.sensor_connected:
            try:
                voltage = self.ina219.bus_voltage
                self.voltage_label.config(text=f"Voltage: {voltage:.2f} V")
                self.voltage_readings.append(voltage)
                self.time_stamps.append(time.time() - self.start_time)
            except Exception as e:
                self.voltage_label.config(text="Error reading voltage")
                print(f"Error: {e}")
        else:
            self.voltage_label.config(text="Error: INA219 not connected")
        self.after(1000, self.update_voltage)  # Update every 1 second

    def show_dashboard(self):
        dashboard_window = tk.Toplevel(self)
        dashboard_window.title("Voltage Dashboard")
        dashboard_window.geometry("800x600")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(self.time_stamps, self.voltage_readings, label="Voltage (V)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title("Voltage Readings Over Time")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoltmeterPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
