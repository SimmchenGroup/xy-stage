from serial_comm import SerialComm

class MotorControl:
    def __init__(self, serial_comm: SerialComm):
        self.serial_comm = serial_comm

    def stop(self):
        self.serial_comm.send_command("S")

    def set_speed_x(self, speed: int):
        sign = "+" if speed >= 0 else "-"
        self.serial_comm.send_command(f"X{sign}{abs(speed)}")

    def set_speed_y(self, speed: int):
        sign = "+" if speed >= 0 else "-"
        self.serial_comm.send_command(f"Y{sign}{abs(speed)}")

    def move_x(self, steps: int, sign):
        self.serial_comm.send_command(f"Xm{sign}{abs(steps)}")

    def move_y(self, steps: int, sign):
        self.serial_comm.send_command(f"Ym{sign}{abs(steps)}")

    def parse_and_send_motor_command(self, cmd: str):
        """
        Parses a command string and dispatches to the proper method.
        Supports speed commands: "X+100", "Y-100"
        And movement commands: "Xm+100", "Ym-50"
        """
        cmd = cmd.strip()
        if cmd.startswith("Xm") or cmd.startswith("Ym"):
            # Movement command detected
            axis = cmd[:2]  # "Xm" or "Ym"
            if len(cmd) < 3 or cmd[2] not in "+-":
                print("Malformed movement command.")
                return
            try:
                value = int(cmd[3:])
            except ValueError:
                print("Invalid numeric value in movement command.")
                return

            if axis == "Xm":
                self.move_x(value, cmd[2])
            elif axis == 'Ym':
                self.move_y(value, cmd[2])
        elif cmd.startswith("X") or cmd.startswith("Y"):
            # Speed command detected
            axis = cmd[0]  # "X" or "Y"
            if len(cmd) < 2 or cmd[1] not in "+-":
                print("Malformed speed command.")
                return
            try:
                value = int(cmd[2:])
            except ValueError:
                print("Invalid numeric value in speed command.")
                return

            if axis == "X":
                self.set_speed_x(value if cmd[1] == "+" else -value)
            else:  # "Y"
                self.set_speed_y(value if cmd[1] == "+" else -value)