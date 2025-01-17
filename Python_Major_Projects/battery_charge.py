import tkinter as tk

class BatteryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Battery Charging Animation")
        self.geometry("300x250")

        # Create a Canvas for the battery drawing
        self.canvas = tk.Canvas(self, width=200, height=100, bg="white")
        self.canvas.pack(pady=20)

        # Draw the battery
        self.battery_outline = self.canvas.create_rectangle(20, 20, 180, 60, outline="black", width=2)
        self.battery_cap = self.canvas.create_rectangle(180, 30, 190, 50, outline="black", width=2)
        self.battery_fill = self.canvas.create_rectangle(22, 22, 22, 58, fill="green", outline="green")

        # Status label
        self.status_label = tk.Label(self, text="Charge: 0%", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

        # Buttons to control charging and draining
        self.start_button = tk.Button(self, text="Start", command=self.start_charging)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_charging)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.drain_button = tk.Button(self, text="Drain", command=self.start_drain)
        self.drain_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.charging = False
        self.drain = False
        self.fill_width = 0
        self.max_fill_width = 158
        self.animation_speed = 5
        self.animation_id = None

    def start_charging(self):
        if not self.charging and not self.drain:
            self.charging = True
            self.update_status(0)
            self.animate_charging()

    def stop_charging(self):
        self.charging = False
        self.drain = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None

    def start_drain(self):
        if not self.drain and not self.charging:
            self.drain = True
            self.update_status(int((self.fill_width / self.max_fill_width) * 100))
            self.animate_drain()

    def animate_charging(self):
        if self.charging:
            if self.fill_width < self.max_fill_width:
                self.fill_width += self.animation_speed
                if self.fill_width > self.max_fill_width:
                    self.fill_width = self.max_fill_width
                self.update_battery_color()
                self.canvas.coords(self.battery_fill, 22, 22, 22 + self.fill_width, 58)
                self.update_status(int((self.fill_width / self.max_fill_width) * 100))
                self.animation_id = self.after(50, self.animate_charging)
            else:
                # When fully charged, stop charging animation
                self.charging = False

    def animate_drain(self):
        if self.drain:
            if self.fill_width > 0:
                self.fill_width -= self.animation_speed
                if self.fill_width < 0:
                    self.fill_width = 0
                self.update_battery_color()
                self.canvas.coords(self.battery_fill, 22, 22, 22 + self.fill_width, 58)
                self.update_status(int((self.fill_width / self.max_fill_width) * 100))
                self.animation_id = self.after(50, self.animate_drain)
            else:
                # When battery is empty, stop draining animation
                self.drain = False

    def update_battery_color(self):
        percentage = (self.fill_width / self.max_fill_width) * 100
        if percentage > 30:
            color = "green"
        elif percentage > 20:
            color = "yellow"
        else:
            color = "red"
        self.canvas.itemconfig(self.battery_fill, fill=color, outline=color)

    def update_status(self, percentage):
        self.status_label.config(text=f"Charge: {percentage}%")

if __name__ == "__main__":
    app = BatteryApp()
    app.mainloop()
