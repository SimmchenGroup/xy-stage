import serial
import time

def initialise_serial():
    # Replace 'COM3' with your Arduino port (e.g., '/dev/ttyUSB0' on Linux)
    arduino_port = 'COM6'
    baud_rate = 115200
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset after serial opens
        print("Arduino Connected")
    except Exception as e:
        print(f"Error opening serial port: {e}")
        exit()

def send_command(cmd):
    print(f"Sending command: {cmd}")
    ser.write((cmd + '\n').encode())  # Send command with newline
    time.sleep(0.1)  # Wait a bit for Arduino to process

    # Read response lines (if any)
    while ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        if response:
            print(f"Arduino response: {response}")

try:
    while True:
        cmd = input("Enter command to send: ")
        if cmd == "exit":
            break
        ser.write((cmd + '\n').encode())  # Send command + newline
        # Optionally read response
        response = ser.readline().decode().strip()
        if response:
            print(f"Arduino says: {response}")

finally:
    ser.close()
