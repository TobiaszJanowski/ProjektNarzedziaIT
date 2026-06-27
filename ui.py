import sys, os
if getattr(sys, 'frozen', False):
    sys.path.append(os.path.dirname(sys.executable))
else:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import converter
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal
class ConvertWorker(QThread):
    finished = pyqtSignal(str)
    def run(self):
        try:
            data = converter.load_data("in.json")
            converter.save_data(data, "out.yml")
            self.finished.emit("Sukces!")
        except Exception as e:
            self.finished.emit(f"Błąd: {str(e)}")
class App(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.btn = QPushButton("Konwertuj")
        self.btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.btn)
        self.setLayout(layout)
    def start_conversion(self):
        self.worker = ConvertWorker()
        self.worker.finished.connect(lambda msg: print(msg))
        self.worker.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec())