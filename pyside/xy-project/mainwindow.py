from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
import imagingcontrol4 as ic4
import numpy as np
import cv2
from PySide6.QtGui import QImage, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IC4 + OpenCV Demo")

        self.label = QLabel("Camera Preview")
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.init_camera()

    def init_camera(self):
        self.grabber = ic4.Grabber()
        self.grabber.device_open(ic4.DeviceEnum.devices()[0])
        self.grabber.device_property_map.set_value(ic4.PropId.WIDTH, 640)
        self.grabber.device_property_map.set_value(ic4.PropId.HEIGHT, 480)

        self.sink = ic4.SnapSink()
        self.grabber.stream_setup(self.sink, display=None, setup_option=ic4.StreamSetupOption.ACQUISITION_START)

        self.timer = self.startTimer(30)  # ~30 FPS

    def timerEvent(self, event):
        buffer = self.grabber.get_buffer()
        data = buffer.get_data()
        frame = buffer.numpy_wrap()

        qimg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        self.grabber.stream_stop()
        self.grabber.device_close()