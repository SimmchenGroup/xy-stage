import serial
import time
import threading

class SerialComm:
    def __init__(self, port, baudrate=115200, timeout=0.1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

        self.callbacks = []
        self.listener_thread = threading.Thread(target=self.read_loop, daemon=True)
        self.listener_thread.start()

    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # wait for Arduino reset
            print(f"Opened serial port {self.port}")
        except Exception as e:
            print(f"Failed to open serial port {self.port}: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Closed serial port: {self.port}")

    def send_command(self, cmd: str):
        if self.ser and self.ser.is_open:
            full_cmd = cmd.strip() + "\n"
            self.ser.write(full_cmd.encode())
            # print(f"Sent: {full_cmd.strip()}")
            # # Read response lines (if any)    # Get rid if needed
            # response = self.ser.readline().decode().strip()
            # if response:
            #     print(f"Received: {response}")

    def read_line(self):
        if self.ser and self.ser.is_open and self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8').strip()
            return line
        return None

    def read_loop(self):
        while True:
            try:
                if self.ser and self.ser.in_waiting:
                    line = self.ser.readline().decode().strip()
                    if line:
                        print(f"Received: {line}")
                        for callback in self.callbacks:
                            callback(line)
            except Exception as e:
                print(f"Serial Read Error: {e}")
                break


    def on_receive(self, callback):
        self.callbacks.append(callback)