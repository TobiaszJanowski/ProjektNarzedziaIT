import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal
from converter import load_data, save_data

class ConvertWorker(QThread):
    finished = pyqtSignal(str)
    def __init__(self, src, dst):
        super().__init__()
        self.src, self.dst = src, dst
    def run(self):
        try:
            data = load_data(self.src)
            save_data(data, self.dst)
            self.finished.emit("Sukces!")
        except Exception as e:
            self.finished.emit(f"Błąd: {str(e)}")

class App(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.btn = QPushButton("Konwertuj (Asynchronicznie)")
        self.btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.btn)
        self.setLayout(layout)
    def start_conversion(self):
        self.worker = ConvertWorker("in.json", "out.yml")
        self.worker.finished.connect(lambda msg: print(msg))
        self.worker.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec())
