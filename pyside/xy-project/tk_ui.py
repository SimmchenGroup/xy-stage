import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from serial_comm import SerialComm
from motor_control import MotorControl

class MotorUI:
    def __init__(self, master, motor_ctrl: MotorControl):
        self.master = master
        self.motor_ctrl = motor_ctrl

        master.title("Motor Control Interface")

        # Set up speed/sensitivity control (for motor moves via arrow keys)
        self.step_label = tk.Label(master, text="Step Size:")
        self.step_label.pack(pady=5)
        self.step_size = tk.IntVar(value=300)
        self.step_scale = tk.Scale(master, from_=10, to=1000, orient="horizontal",
                                   variable=self.step_size)
        self.step_scale.pack(pady=5)

        # Bind keyboard events to movement functions
        master.bind("<Left>", self.move_left)
        master.bind("<Right>", self.move_right)
        master.bind("<Up>", self.move_up)
        master.bind("<Down>", self.move_down)

        # Control buttons
        self.stop_button = tk.Button(master, text="Stop", command=self.motor_ctrl.stop)
        self.stop_button.pack(pady=5)

        # Command entry field to send arbitrary commands
        entry_frame = tk.Frame(master)
        entry_frame.pack(pady=5)
        self.command_entry = tk.Entry(entry_frame, width=40)
        self.command_entry.pack(side=tk.LEFT, padx=(0,5))
        self.send_button = tk.Button(entry_frame, text="Send", command=self.send_command)
        self.send_button.pack(side=tk.LEFT)

        # Create a scrolled text widget for displaying the serial monitor output
        self.monitor_text = ScrolledText(master, width=60, height=15, state="disabled")
        self.monitor_text.pack(pady=5)

        # Begin periodic update of serial messages in the UI
        self.update_serial_monitor()

    # Movement functions (expect motor_ctrl methods that accept step & direction)
    def move_left(self, event):
        step = self.step_size.get()
        self.motor_ctrl.move_x(step, "-")

    def move_right(self, event):
        step = self.step_size.get()
        self.motor_ctrl.move_x(step, "+")

    def move_up(self, event):
        step = self.step_size.get()
        self.motor_ctrl.move_y(step, "+")

    def move_down(self, event):
        step = self.step_size.get()
        self.motor_ctrl.move_y(step, "-")

    def send_command(self):
        """Send the contents of the entry field as a command via MotorControl."""
        cmd = self.command_entry.get().strip()
        if cmd:
            # Optionally, you can also display the command in the monitor area
            self.append_to_monitor(f"Sending command: {cmd}")
            self.motor_ctrl.parse_and_send_motor_command(cmd)
            # Clear the entry after sending
            self.command_entry.delete(0, tk.END)

    def append_to_monitor(self, text):
        """Helper function to append text to the serial monitor output widget."""
        self.monitor_text.config(state="normal")
        self.monitor_text.insert("end", text + "\n")
        self.monitor_text.see("end")
        self.monitor_text.config(state="disabled")

    def update_serial_monitor(self):
        """Poll the serial port for new messages and display them in the UI."""
        line = self.motor_ctrl.serial_comm.read_line()
        if line:
            self.append_to_monitor(line)
        # Schedule next update after 50 ms
        self.master.after(50, self.update_serial_monitor)