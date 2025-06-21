from motor_control import MotorControl
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout
)

class MainWindow(QMainWindow):
    def __init__(self, motor_ctrl: MotorControl):
        super().__init__()

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.motor_ctrl = motor_ctrl

        self.speed_interval = 10
        self.speed_min = 0
        self.speed_max = 100

        self.step_interval = 50
        self.step_min = 0
        self.step_max = 1000

        # Here is all the creation of the Window or 'parent' as I probably incorrectly call it
        self.setWindowTitle("XY-Stage Control")
        self.setFixedSize(700,700)
        self.setWindowOpacity(1.0)
        parent_layout = QHBoxLayout()

        # Create the widgets finishing with the layout
        # Slider widgets - These could maybe unified into a create generic slider function
        self.speed_label = QLabel(f"Speed : {self.speed_min}")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(self.speed_min, self.speed_max)
        self.snap_slider(self.speed_slider, self.speed_interval)
        self.speed_slider.setTickInterval(self.speed_interval)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)

        self.step_label = QLabel(f"Step-Size : {self.step_min}")
        self.step_slider = QSlider(Qt.Horizontal)
        self.step_slider.setRange(self.step_min, self.step_max)
        self.snap_slider(self.step_slider, self.step_interval)
        self.step_slider.setTickInterval(self.step_interval)
        self.step_slider.valueChanged.connect(self.update_step_label)
        self.step_slider.setTickPosition(QSlider.TicksBelow)


        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.speed_label)
        slider_layout.addWidget(self.speed_slider)
        slider_layout.addWidget(self.step_label)
        slider_layout.addWidget(self.step_slider)

        parent_layout.addLayout(slider_layout)

        # Push Buttons UP DOWN LEFT RIGHT

        container = QWidget()
        container.setLayout(parent_layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        step = self.step_slider.value()
        key = event.key()
        if key == Qt.Key_A:
            self.motor_ctrl.move_x(step, "-")
        elif key == Qt.Key_D:
            self.motor_ctrl.move_x(step, "+")
        elif key == Qt.Key_W:
            self.motor_ctrl.move_y(step, "+")
        elif key == Qt.Key_S:
            self.motor_ctrl.move_y(step, "-")
        elif key == Qt.Key_Up:
            self.motor_ctrl.set


    def snap_slider(self, slider: QSlider, step: int):
        def snap(value):
            snapped = round(value / step) * step
            if value != snapped:
                slider.blockSignals(True)  # Prevent recursive signal loop
                slider.setValue(snapped)  # Force thumb to snap visually
                slider.blockSignals(False)

        slider.valueChanged.connect(snap)

    def snap_to_interval(self, value, interval):
        return  round(value / interval) * interval
    def update_speed_label(self, value):
        snapped = self.snap_to_interval(value, self.speed_interval)
        self.speed_label.setText(f"Speed : {snapped}")

    def update_step_label(self, value):
        snapped = self.snap_to_interval(value, self.step_interval)
        self.step_label.setText(f"Step-Size: {snapped}")


