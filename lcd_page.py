import tkinter as tk
from PIL import Image, ImageTk
from header import Header
from datetime import datetime
import adafruit_character_lcd.character_lcd as characterlcd
import board
import digitalio
import time

class LCDPage(tk.Frame):
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

        welcome_text = "Enter Reference"
        self.canvas.create_text(400, 100, text=welcome_text, font=("Helvetica", 16), fill="black", justify="center", anchor="n")

        self.input_var = tk.StringVar()
        entry = tk.Entry(self.canvas, textvariable=self.input_var, font=("Helvetica", 14))
        entry.place(relx=0.5, rely=0.3, anchor="center")
        
        button_send = tk.Button(self.canvas, text="Send", font=("Helvetica", 14), bg="white", fg="black", command=self.send_to_lcd)
        button_send.place(relx=0.3, rely=0.4, anchor="center")
        
        button_save = tk.Button(self, text="Save", font=("Helvetica", 14), bg="white", fg="black", command=self.save_data)
        button_save.place(relx=0.5, rely=0.435, anchor="center")
        
        button_clear = tk.Button(self.canvas, text="Clear", font=("Helvetica", 14), bg="white", fg="black", command=self.clear_lcd)
        button_clear.place(relx=0.7, rely=0.4, anchor="center")
        
        button_show_data = tk.Button(self.canvas, text="Show Data", font=("Helvetica", 14), bg="white", fg="black", command=self.show_data)
        button_show_data.place(relx=0.5, rely=0.6, anchor="center")
    
        footer_text = "© All rights reserved Sagemcom"
        self.canvas.create_text(400, 500, text=footer_text, font=("Helvetica", 16), fill="black", justify="center", anchor="s")

        # Setup the LCD
        self.lcd_columns = 16
        self.lcd_rows = 2

        # Modify this section with the correct GPIO pins for your setup
        lcd_rs = digitalio.DigitalInOut(board.D4)  # GPIO 4
        lcd_en = digitalio.DigitalInOut(board.D17)  # GPIO 17
        lcd_d4 = digitalio.DigitalInOut(board.D18)  # GPIO 18
        lcd_d5 = digitalio.DigitalInOut(board.D27)  # GPIO 27
        lcd_d6 = digitalio.DigitalInOut(board.D22)  # GPIO 22
        lcd_d7 = digitalio.DigitalInOut(board.D23)  # GPIO 23

        self.lcd = characterlcd.Character_LCD_Mono(
            lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, self.lcd_columns, self.lcd_rows
        )

    def save_data(self):
        input_text = self.input_var.get()
        if input_text:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("data.txt", "a") as file:
                file.write(f"{current_date}: {input_text}\n")

    def show_data(self):
        # Create a new window for displaying data
        data_window = tk.Toplevel(self)
        data_window.title("Data from data.txt")
        data_window.geometry("500x400")

        # Create a frame to hold the text box and buttons
        frame = tk.Frame(data_window, bg="white", bd=2, relief="sunken")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a text widget to display the data
        self.text_widget = tk.Text(frame, wrap="none")
        self.text_widget.pack(fill="both", expand=True)

        # Create a vertical scrollbar for the text widget
        scrollbar_y = tk.Scrollbar(self.text_widget, orient="vertical", command=self.text_widget.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.text_widget.config(yscrollcommand=scrollbar_y.set)

        # Create a horizontal scrollbar for the text widget
        scrollbar_x = tk.Scrollbar(self.text_widget, orient="horizontal", command=self.text_widget.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        self.text_widget.config(xscrollcommand=scrollbar_x.set)

        # Read the data from data.txt and insert it into the text widget
        self.load_data()

        # Create Save and Delete buttons
        button_frame = tk.Frame(data_window)
        button_frame.pack(fill="x", padx=10, pady=5)

        button_save_changes = tk.Button(button_frame, text="Save Changes", command=self.save_changes)
        button_save_changes.pack(side="left", padx=5)

        button_delete_line = tk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        button_delete_line.pack(side="left", padx=5)

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if ": " in line:
                        date_time, reference = line.split(": ", 1)
                        self.text_widget.insert("end", f"{date_time}: ")
                        self.text_widget.insert("end", reference, "editable")
                        self.text_widget.insert("end", "\n")
                self.text_widget.tag_configure("editable", foreground="black")
                self.text_widget.tag_configure("readonly", foreground="gray")
                self.make_readonly()
        except FileNotFoundError:
            self.text_widget.insert("1.0", "No data found. 'data.txt' file does not exist.")

    def make_readonly(self):
        # Iterate through each line to disable editing for date and time
        lines = self.text_widget.get("1.0", "end-1c").split("\n")
        for line_num, line in enumerate(lines, 1):
            if ": " in line:
                date_time, reference = line.split(": ", 1)
                self.text_widget.tag_add("readonly", f"{line_num}.0", f"{line_num}.{len(date_time) + 2}")

        self.text_widget.tag_configure("readonly", foreground="gray")
        self.text_widget.tag_bind("readonly", "<KeyPress>", lambda e: "break")
        self.text_widget.tag_bind("readonly", "<Button-1>", lambda e: "break")

    def save_changes(self):
        data = self.text_widget.get("1.0", "end-1c").split("\n")
        with open("data.txt", "w") as file:
            for line in data:
                file.write(line + "\n")

    def delete_selected(self):
        selected_text = self.text_widget.tag_ranges(tk.SEL)
        if selected_text:
            self.text_widget.delete(selected_text[0], selected_text[1])

    def send_to_lcd(self):
        text = self.input_var.get()
        if len(text) > self.lcd_columns:
            self.scroll_text(text)
        else:
            self.lcd.clear()
            self.lcd.message = text

    def clear_lcd(self):
        self.lcd.clear()

    def scroll_text(self, text):
        display_text = text + " " * self.lcd_columns  # Add spaces to create a gap
        for i in range(len(text) + self.lcd_columns):
            self.lcd.clear()
            self.lcd.message = display_text[i:i + self.lcd_columns]
            time.sleep(0.3)  # Adjust the delay to control scrolling speed

if __name__ == "__main__":
    root = tk.Tk()
    app = LCDPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
