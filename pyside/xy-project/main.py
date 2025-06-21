import tkinter as tk
from serial_comm import SerialComm
from motor_control import MotorControl
from tk_ui import MotorUI
from motor_UI import MainWindow
from PyQt5.QtWidgets import QApplication
# from camera import Camera  # Uncomment if needed

def main():
    port = "COM6"  # Change to your Arduino port (e.g., "COM3" or "/dev/ttyUSB0")
    serial_comm = SerialComm(port, baudrate=115200, timeout=1)
    serial_comm.open()
    motor_ctrl = MotorControl(serial_comm)

    app = QApplication([])
    window = MainWindow(motor_ctrl)
    window.show()
    app.exec_()
    serial_comm.close()


    # root = tk.Tk()
    # ui = MotorUI(root, motor_ctrl)
    # root.mainloop()
    #
    # # When the UI window is closed, close the serial connection
    # serial_comm.close()
    #

    # try:
    #     while True:
    #         command = input("Enter Command: ").strip()
    #         # Process the input command
    #         if command in "Qqexit":
    #             print("Quitting and closing serial port.")
    #             break
    #         if command == "serialclose":
    #             serial_comm.close()
    #         if command == "serialopen":
    #             serial_comm.open()
    #         motor_ctrl.parse_and_send_motor_command(command)
    #         print(f"Arduino says: {serial_comm.read_line()}")
    # except KeyboardInterrupt:
    #     print("Keyboard interrupt received. Exiting.")
    # finally:
    #     serial_comm.close()


if __name__ == "__main__":
    main()