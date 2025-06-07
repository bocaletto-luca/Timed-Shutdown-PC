# Software Name: Timed Shutdown PC
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it
# License: GPLv3
# Import the tkinter module to create the graphical user interface
import tkinter as tk
from tkinter import ttk
import os
import time
import threading
from tkinter import messagebox

# Define the main application class
class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timed Shutdown PC")  # Set the application title

        # Create a label to display the current time
        self.clock_label = tk.Label(root, text="", font=("Helvetica", 48))
        self.clock_label.pack()

        # Start the clock update
        self.start_clock()

        # Create the interface for scheduling actions
        self.create_schedule_interface()

    def start_clock(self):
        # Function to update the clock in real-time
        def update_clock():
            while True:
                current_time = time.strftime("%H:%M:%S")
                self.clock_label.config(text=current_time)
                time.sleep(1)

        # Create a thread for the clock that runs in the background
        clock_thread = threading.Thread(target=update_clock)
        clock_thread.daemon = True  # The thread will terminate when the app is closed
        clock_thread.start()

    def create_schedule_interface(self):
        # Create a frame for the scheduling interface
        schedule_frame = ttk.LabelFrame(self.root, text="Schedule")
        schedule_frame.pack(padx=20, pady=20)

        # Label for entering the time
        time_label = ttk.Label(schedule_frame, text="Time (HH:MM):")
        time_label.grid(row=0, column=0, padx=10, pady=10)

        # Text entry box for entering the time
        self.time_entry = ttk.Entry(schedule_frame)
        self.time_entry.grid(row=0, column=1, padx=10, pady=10)

        # Variable to store the selected action
        self.action_var = tk.StringVar()
        self.action_var.set("Shutdown")  # Set the default action to "Shutdown"

        # Buttons for different actions
        shutdown_button = ttk.Button(schedule_frame, text="Shutdown", command=self.shutdown_system)
        shutdown_button.grid(row=1, column=0, padx=10, pady=10)

        restart_button = ttk.Button(schedule_frame, text="Restart", command=self.restart_system)
        restart_button.grid(row=1, column=1, padx=10, pady=10)

        suspend_button = ttk.Button(schedule_frame, text="Suspend", command=self.suspend_system)
        suspend_button.grid(row=2, column=0, padx=10, pady=10)

        schedule_button = ttk.Button(schedule_frame, text="Schedule", command=self.schedule_action)
        schedule_button.grid(row=2, column=1, padx=10, pady=10)

    def schedule_action(self):
        # Function to schedule an action
        scheduled_time = self.time_entry.get()

        if not scheduled_time:
            # If the time is not entered, show an error message
            messagebox.showerror("Error", "Please enter a valid time before scheduling an action.")
            return

        try:
            hh, mm = map(int, scheduled_time.split(':'))
            today_time = time.localtime()
            scheduled_time = time.mktime((today_time.tm_year, today_time.tm_mon, today_time.tm_mday, hh, mm, 0, -1, -1, -1))
            current_time = time.mktime(time.localtime())
            delay = scheduled_time - current_time

            if delay <= 0:
                # If the time is in the past, show an error message
                messagebox.showerror("Error", "Please enter a valid future time.")
            else:
                # Wait for the delay and then execute the scheduled action
                self.root.after(int(delay * 1000), self.execute_action)
        except ValueError:
            # If the time is in an invalid format, show an error message
            messagebox.showerror("Error", "Invalid time format (HH:MM).")

    def execute_action(self):
        # Function to execute the scheduled action
        selected_action = self.action_var.get()
        if selected_action == "Shutdown":
            os.system("shutdown /s /f /t 0")  # Shutdown the system
        elif selected_action == "Restart":
            os.system("shutdown /r /f /t 0")  # Restart the system
        elif selected_action == "Suspend":
            os.system("shutdown /h /f")  # Suspend the system

    def shutdown_system(self):
        self.action_var.set("Shutdown")

    def restart_system(self):
        self.action_var.set("Restart")

    def suspend_system(self):
        self.action_var.set("Suspend")

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()  # Start the main user interface
