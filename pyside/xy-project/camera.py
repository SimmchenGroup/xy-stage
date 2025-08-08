import imagingcontrol4 as ic4
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

def demoapp_main():
    # Initialize IC4 within a context manager
    with ic4.Library.init_context():
        app = QApplication()
        app.setApplicationName("ic4-demoapp")
        app.setApplicationDisplayName("IC4 Demo Application")
        app.setStyle("fusion")

        # Create and show your main window
        w = MainWindow()
        w.show()

        # Start the Qt event loop
        app.exec()

if __name__ == "__main__":
    demoapp_main()