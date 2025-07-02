import customtkinter as ctk
from tkinter import messagebox

class TemperatureConverterApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("ThermoConvert")
        self.window.geometry("500x450")
        self.window.resizable(False, False)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(pady=30, padx=40, fill="both", expand=True)

        header = ctk.CTkLabel(
            main_frame,
            text="Temperature Converter",
            font=("Arial", 24, "bold")
        )
        header.pack(pady=(0, 20))

        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=10)

        self.temp_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter temperature",
            width=180,
            height=40,
            font=("Arial", 16)
        )
        self.temp_entry.pack(side="left", padx=(0, 10))

        self.unit_var = ctk.StringVar(value="Celsius")
        unit_menu = ctk.CTkOptionMenu(
            input_frame,
            variable=self.unit_var,
            values=["Celsius", "Fahrenheit", "Kelvin"],
            width=120,
            height=40,
            font=("Arial", 14),
            dropdown_font=("Arial", 14)
        )
        unit_menu.pack(side="left")

        convert_btn = ctk.CTkButton(
            main_frame,
            text="Convert",
            command=self.convert_temperature,
            height=45,
            font=("Arial", 16, "bold"),
            corner_radius=8
        )
        convert_btn.pack(pady=20, fill="x")

        results_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, pady=10)

        result_style = {"font": ("Arial", 18), "anchor": "w", "padx": 20}
        
        self.celsius_result = ctk.CTkLabel(results_frame, text="Celsius: ", **result_style)  # 🔧 NEW
        self.celsius_result.pack(fill="x", pady=8)

        self.fahrenheit_result = ctk.CTkLabel(results_frame, text="Fahrenheit: ", **result_style)
        self.fahrenheit_result.pack(fill="x", pady=8)

        self.kelvin_result = ctk.CTkLabel(results_frame, text="Kelvin: ", **result_style)
        self.kelvin_result.pack(fill="x", pady=8)

        ctk.CTkFrame(main_frame, height=2, fg_color="#333").pack(fill="x", pady=15)
        footer = ctk.CTkLabel(main_frame, text="Enter any temperature value to convert", font=("Arial", 12))
        footer.pack()

    def convert_temperature(self):
        input_temp = self.temp_entry.get()
        selected_unit = self.unit_var.get()

        try:
            temperature = float(input_temp)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number")
            return

        # 🔧 Convert all values
        if selected_unit == "Celsius":
            celsius = temperature
            fahrenheit = (temperature * 9 / 5) + 32
            kelvin = temperature + 273.15
        elif selected_unit == "Fahrenheit":
            celsius = (temperature - 32) * 5 / 9
            fahrenheit = temperature
            kelvin = celsius + 273.15
        elif selected_unit == "Kelvin":
            celsius = temperature - 273.15
            fahrenheit = (celsius * 9 / 5) + 32
            kelvin = temperature

        # 🔧 Update all three result labels
        self.celsius_result.configure(text=f"Celsius: {celsius:.2f}°C")
        self.fahrenheit_result.configure(text=f"Fahrenheit: {fahrenheit:.2f}°F")
        self.kelvin_result.configure(text=f"Kelvin: {kelvin:.2f}K")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TemperatureConverterApp()
    app.run()
