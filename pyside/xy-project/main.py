import time
from serial_comm import SerialComm
from motor_control import MotorControl
# from camera import Camera  # Uncomment if needed

def main():
    port = "COM6"  # Change to your Arduino port (e.g., "COM3" or "/dev/ttyUSB0")
    serial_comm = SerialComm(port, baudrate=115200, timeout=1)
    serial_comm.open()

    # If you wish to use MotorControl commands, you can create an instance:
    motor_ctrl = MotorControl(serial_comm)
    # You can also instantiate other classes like Camera if needed.

    print("Arduino Connected. Enter command to send (type 'exit' or 'Q' to quit):")

    try:
        while True:
            command = input("Enter Command: ").strip()
            # Process the input command
            if command in "Qqexit":
                print("Quitting and closing serial port.")
                break
            if command == "serialclose":
                serial_comm.close()
            if command == "serialopen":
                serial_comm.open()
            motor_ctrl.parse_and_send_motor_command(command)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting.")
    finally:
        serial_comm.close()


if __name__ == "__main__":
    main()