import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QLabel, QVBoxLayout, QWidget, QScrollArea
from PyQt5.QtGui import QPixmap
import fitz  # PyMuPDF

class EbookReader(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Window
        self.setWindowTitle("Yumi's EbookReader")
        self.setGeometry(100, 100, 800, 600)

        # Menu
        openFile = QAction('Open Ebook', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.open_ebook)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

    def open_ebook(self):
        ebook_path, _ = QFileDialog.getOpenFileName(self, 'Open Ebook', '', 'PDF Files (*.pdf)')
        if ebook_path:
            if ebook_path.endswith('.pdf'):
                self.load_pdf(ebook_path)

    def load_pdf(self, path):
        try:
            doc = fitz.open(path)
            layout = QVBoxLayout()

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap() 
                
                img_data = pix.tobytes("png")  
                img = QPixmap()
                img.loadFromData(img_data)
                
                label = QLabel(self)
                label.setPixmap(img)
                layout.addWidget(label)

            container = QWidget()
            container.setLayout(layout)

            scroll_area = QScrollArea(self)
            scroll_area.setWidget(container)
            scroll_area.setWidgetResizable(True)

            self.setCentralWidget(scroll_area)

            print("Successfully loaded PDF as images.")
        except Exception as e:
            print(f"Error loading PDF: {str(e)}")

# Main Loop
app = QApplication(sys.argv)
window = EbookReader()
window.show()
sys.exit(app.exec_())
