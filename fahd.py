import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FileManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Manager")
        self.resize(500,600)

        self.folder = os.getcwd()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.title = QLabel("Files")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:24px;")

        self.layout.addWidget(self.title)

        self.list = QListWidget()
        self.layout.addWidget(self.list)

        buttons = QHBoxLayout()

        self.upload = QPushButton("Upload")
        self.delete = QPushButton("Delete")
        self.refresh = QPushButton("Refresh")

        buttons.addWidget(self.upload)
        buttons.addWidget(self.delete)
        buttons.addWidget(self.refresh)

        self.layout.addLayout(buttons)

        self.upload.clicked.connect(self.upload_file)
        self.delete.clicked.connect(self.delete_file)
        self.refresh.clicked.connect(self.load_files)

        self.list.itemDoubleClicked.connect(self.open_file)

        self.setStyleSheet("""

        QMainWindow{
        background:#0f172a;
        }

        QLabel{
        color:white;
        }

        QListWidget{
        background:#1e293b;
        color:white;
        border-radius:15px;
        padding:10px;
        }

        QPushButton{
        background:#3b82f6;
        color:white;
        border:none;
        padding:10px;
        border-radius:10px;
        }

        QPushButton:hover{
        background:#2563eb;
        }

        """)

        self.load_files()

    def load_files(self):
        self.list.clear()
        for f in os.listdir(self.folder):
            self.list.addItem(f)

    def upload_file(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select File")
        if file:
            name = os.path.basename(file)
            with open(file,"rb") as src:
                with open(name,"wb") as dst:
                    dst.write(src.read())
        self.load_files()

    def delete_file(self):
        item = self.list.currentItem()
        if item:
            os.remove(item.text())
        self.load_files()

    def open_file(self,item):
        os.startfile(item.text())

app = QApplication(sys.argv)
window = FileManager()
window.show()
sys.exit(app.exec_())
