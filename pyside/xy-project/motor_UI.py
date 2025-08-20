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

        self.held_keys = set()  # keep track of which keys are currently held down.

        self.speed_interval = 100
        self.speed_min = 300
        self.speed_max = 2500

        self.step_interval = 100
        self.step_min = 100
        self.step_max = 2500

        # Here is all the creation of the Window or 'parent' as I probably incorrectly call it
        self.setWindowTitle("XY-Stage Control")
        self.setFixedSize(700,700)
        self.setWindowOpacity(1.0)
        parent_layout = QHBoxLayout()

        # Create the widgets finishing with the layout
        # Slider widgets - These could maybe unified into a create generic slider function
        self.speed_label = QLabel(f"Speed : {self.speed_min}")
        self.label_styler((self.speed_label))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(self.speed_min, self.speed_max)
        self.snap_slider(self.speed_slider, self.speed_interval)
        self.speed_slider.setTickInterval(self.speed_interval)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.slider_styler(self.speed_slider)

        self.step_label = QLabel(f"Step-Size : {self.step_min}")
        self.label_styler(self.step_label)
        self.step_slider = QSlider(Qt.Horizontal)
        self.step_slider.setRange(self.step_min, self.step_max)
        self.snap_slider(self.step_slider, self.step_interval)
        self.slider_styler(self.step_slider)
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
        if event.isAutoRepeat():
            return

        step = self.step_slider.value()
        speed = self.speed_slider.value()
        key = event.key()
        if key in self.held_keys:
            return   #this will ignore repeats
        self.held_keys.add(key)
        if key == Qt.Key_A:
            self.motor_ctrl.displace_x(step, "+")
        elif key == Qt.Key_D:
            self.motor_ctrl.displace_x(step, "-")
        elif key == Qt.Key_W:
            self.motor_ctrl.displace_y(step, "+")
        elif key == Qt.Key_S:
            self.motor_ctrl.displace_y(step, "-")
        elif key == Qt.Key_J:
            self.motor_ctrl.move_x(speed, "+")
        elif key == Qt.Key_L:
            self.motor_ctrl.move_x(speed, "-")
        elif key == Qt.Key_I:
            self.motor_ctrl.move_y(speed, "+")
        elif key == Qt.Key_K:
            self.motor_ctrl.move_y(speed, "-")

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return                  # Ignores 'fake' releases
        key = event.key()
        self.held_keys.discard(key)
        if key in {Qt.Key_J, Qt.Key_L}:
            self.motor_ctrl.move_x(0, "+")
        elif key in {Qt.Key_I, Qt.Key_K}:
            self.motor_ctrl.move_y(0, "+")

    def label_styler(self, label: QLabel):
        label.setStyleSheet("""
            QLabel {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 32px;
                color: #f0f0f0;
                background-color: #1e1e1e;
                padding: 6px 10px;
                border: 2px solid #444;
                border-radius: 6px;
            }
        """)

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
        self.motor_ctrl.set_speed(snapped)

    def update_step_label(self, value):
        snapped = self.snap_to_interval(value, self.step_interval)
        self.step_label.setText(f"Step-Size: {snapped}")

    def slider_styler(self, slider: QSlider):
        slider.setMinimumHeight(200)

        slider.setStyleSheet("""
               QSlider::groove:horizontal {
                   background: #2b2b2b;
                   height: 20px;
                   border-radius: 10px;
               }
    
               QSlider::handle:horizontal {
                   background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                               stop:0 #f90, stop:1 #c60);
                   width: 90px;
                   height: 60px;
                   margin: -9px 0;
                   border-radius: 15px;
                   border: 7px solid #111;
               }
    
               QSlider::sub-page:horizontal {
                   background: green;
                   border-radius: 7px; 
               }
    
               QSlider::add-page:horizontal {
                   background: red;
                   border-radius: 7px;
               }
    
               QSlider::tick-mark:horizontal {
                   background: #ccc;
                   height: 8px;
               }
           """)
