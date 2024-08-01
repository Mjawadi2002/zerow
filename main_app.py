import tkinter as tk
from home_page import HomePage
from first_page import FirstPage
from sensors_page import SensorsPage
from lcd_page import LCDPage
from powermeter_page import PowermeterPage
from voltmeter_page import VoltmeterPage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Setup matplotlib figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r-', label='Power')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 5)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Power (W)')
        self.ax.set_title('Power Meter Reading')
        self.ax.legend()
        self.xdata, self.ydata = [], []
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_plot.get_tk_widget().pack(fill="both", expand=True)

        # Button to switch back to the PowermeterPage
        button = tk.Button(self, text="Back to Power Meter", command=lambda: controller.show_frame("PowermeterPage"), font=("Helvetica", 14), bg="white", fg="black", padx=16, pady=10)
        button.pack(side="bottom", pady=10)

    def update_plot(self, xdata, ydata):
        self.xdata = xdata
        self.ydata = ydata
        self.line.set_data(self.xdata, self.ydata)
        if len(self.xdata) > 100:
            self.ax.set_xlim(len(self.xdata) - 100, len(self.xdata))
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas_plot.draw()

class RaspberryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Raspberry app")
        self.geometry("800x600")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (HomePage, FirstPage, SensorsPage, LCDPage, PowermeterPage, VoltmeterPage, PlotPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def update_plot_page(self, xdata, ydata):
        plot_page = self.frames["PlotPage"]
        plot_page.update_plot(xdata, ydata)

if __name__ == "__main__":
    app = RaspberryApp()
    app.mainloop()

