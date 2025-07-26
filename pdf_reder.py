from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
import sys

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF File Picker")
        self.setGeometry(200, 200, 500, 150)

        # Label
        self.label = QLabel("No file selected", self)
        self.label.setGeometry(20, 50, 450, 30)

        # Button to choose file
        self.button = QPushButton("Select PDF", self)
        self.button.setGeometry(20, 10, 120, 30)
        self.button.clicked.connect(self.select_pdf)

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "",
                                                   "Supported Files (*.pdf *.png *.jpg *.jpeg);;PDF Files (*.pdf);;Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.label.setText(f"Selected: {file_path}")
            # You can now process the PDF file using PyPDF2, fitz (PyMuPDF), etc.
        else:
            self.label.setText("No file selected")

def window():
    app = QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())

window()
