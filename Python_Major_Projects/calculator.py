import tkinter as tk
import math

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.configure(bg="#282c34")  # Background color for the main window

        # Create a frame to hold the calculator buttons
        self.button_frame = tk.Frame(self, bg="#282c34")
        self.button_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.button_frame.grid_propagate(False)  # Prevent resizing based on children

        # Create a variable to store the current input
        self.current_input = tk.StringVar()

        # Create a label to display the current input
        self.input_label = tk.Label(self.button_frame, textvariable=self.current_input, font=("Helvetica", 20), anchor="e", bg="#ffffff", fg="#000000", height=2)
        self.input_label.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Button dimensions
        self.button_width = 5
        self.button_height = 2

        # Create a dictionary to map button text to corresponding functions
        button_mapping = {
            "AC": self.clear_input,
            "%": self.calculate_percentage,
            "←": self.delete_last_char,
            "/": lambda: self.append_operator("/"),
            "7": lambda: self.append_digit("7"),
            "8": lambda: self.append_digit("8"),
            "9": lambda: self.append_digit("9"),
            "x": lambda: self.append_operator("*"),
            "4": lambda: self.append_digit("4"),
            "5": lambda: self.append_digit("5"),
            "6": lambda: self.append_digit("6"),
            "-": lambda: self.append_operator("-"),
            "1": lambda: self.append_digit("1"),
            "2": lambda: self.append_digit("2"),
            "3": lambda: self.append_digit("3"),
            "+": lambda: self.append_operator("+"),
            "00": lambda: self.append_digit("00"),
            "0": lambda: self.append_digit("0"),
            ".": self.append_decimal,
            "=": self.calculate_result,
            "Expand": self.toggle_advanced
        }

        # Create buttons and assign them to the corresponding functions
        self.create_buttons(button_mapping)

        # Create an expandable frame for advanced functions
        self.advanced_frame = tk.Frame(self, bg="#282c34")
        self.create_advanced_buttons()
        self.advanced_frame.pack(fill=tk.X, pady=(5, 0))
        self.advanced_frame.grid_propagate(False)  # Prevent resizing based on children

    def create_buttons(self, button_mapping):
        row = 1
        col = 0
        for text, function in button_mapping.items():
            button = tk.Button(self.button_frame, text=text, font=("Helvetica", 16), command=function,
                               bg="#4b4f68", fg="#ffffff", width=self.button_width, height=self.button_height,
                               relief="raised", bd=2)
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col == 4:
                row += 1
                col = 0
        
        # Adjust row and column weights for proper button resizing
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)

    def create_advanced_buttons(self):
        advanced_buttons = {
            "sin": lambda: self.append_function("math.sin"),
            "cos": lambda: self.append_function("math.cos"),
            "tan": lambda: self.append_function("math.tan"),
            "√": lambda: self.append_function("math.sqrt"),
            "log": lambda: self.append_function("math.log"),
            "exp": lambda: self.append_function("math.exp"),
            "π": lambda: self.append_constant("math.pi")
        }

        for text, function in advanced_buttons.items():
            button = tk.Button(self.advanced_frame, text=text, font=("Helvetica", 16), command=function,
                               bg="#4b4f68", fg="#ffffff", width=self.button_width, height=self.button_height,
                               relief="raised", bd=2)
            button.pack(side=tk.LEFT, padx=5, pady=5)

    # Function to clear the input
    def clear_input(self):
        self.current_input.set("")

    # Function to calculate the percentage
    def calculate_percentage(self):
        try:
            value = float(self.current_input.get())
            result = value / 100
            self.current_input.set(str(result))
        except ValueError:
            pass

    # Function to delete the last character
    def delete_last_char(self):
        current_text = self.current_input.get()
        if current_text:
            self.current_input.set(current_text[:-1])

    # Function to append an operator
    def append_operator(self, operator):
        current_text = self.current_input.get()
        if current_text and not current_text[-1] in "+-*/%":
            self.current_input.set(current_text + operator)

    # Function to append a digit
    def append_digit(self, digit):
        current_text = self.current_input.get()
        if current_text == "0":
            self.current_input.set(digit)
        else:
            self.current_input.set(current_text + digit)

    # Function to append a decimal point
    def append_decimal(self):
        if "." not in self.current_input.get():
            self.current_input.set(self.current_input.get() + ".")

    # Function to calculate the result
    def calculate_result(self):
        try:
            expression = self.current_input.get().replace("x", "*")
            result = eval(expression)
            self.current_input.set(str(result))
        except (SyntaxError, ZeroDivisionError):
            self.current_input.set("Error")

    # Function to toggle the advanced section
    def toggle_advanced(self):
        if self.advanced_frame.winfo_ismapped():
            self.advanced_frame.pack_forget()
        else:
            self.advanced_frame.pack(fill=tk.X, pady=(5, 0))

    # Function to append mathematical functions
    def append_function(self, func):
        current_text = self.current_input.get()
        self.current_input.set(current_text + func + "(")

    # Function to append mathematical constants
    def append_constant(self, constant):
        current_text = self.current_input.get()
        self.current_input.set(current_text + constant)

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
