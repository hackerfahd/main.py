import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class IOSFileManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.path = os.getcwd()

        self.setWindowTitle("iOS File Manager")
        self.resize(700,600)

        main = QWidget()
        self.setCentralWidget(main)

        self.layout = QVBoxLayout()
        main.setLayout(self.layout)

        # Top bar
        bar = QHBoxLayout()

        self.back = QPushButton("←")
        self.back.clicked.connect(self.go_back)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search")
        self.search.textChanged.connect(self.load_files)

        self.refresh = QPushButton("⟳")
        self.refresh.clicked.connect(self.load_files)

        bar.addWidget(self.back)
        bar.addWidget(self.search)
        bar.addWidget(self.refresh)

        self.layout.addLayout(bar)

        # File grid
        self.list = QListWidget()
        self.list.setViewMode(QListWidget.IconMode)
        self.list.setIconSize(QSize(64,64))
        self.list.setResizeMode(QListWidget.Adjust)
        self.list.setSpacing(20)
        self.list.itemDoubleClicked.connect(self.open_item)

        self.layout.addWidget(self.list)

        # Bottom buttons
        bottom = QHBoxLayout()

        self.delete = QPushButton("Delete")
        self.delete.clicked.connect(self.delete_file)

        self.up = QPushButton("Upload")
        self.up.clicked.connect(self.upload_file)

        bottom.addWidget(self.delete)
        bottom.addWidget(self.up)

        self.layout.addLayout(bottom)

        self.setStyleSheet("""

        QMainWindow{
        background:#0f172a;
        }

        QListWidget{
        background:#1e293b;
        border-radius:20px;
        padding:20px;
        color:white;
        }

        QPushButton{
        background:#3b82f6;
        border:none;
        padding:8px;
        border-radius:10px;
        color:white;
        }

        QPushButton:hover{
        background:#2563eb;
        }

        QLineEdit{
        background:#1e293b;
        border-radius:10px;
        padding:6px;
        color:white;
        }

        """)

        self.load_files()

    def load_files(self):
        self.list.clear()

        query = self.search.text().lower()

        for f in os.listdir(self.path):

            if query and query not in f.lower():
                continue

            item = QListWidgetItem()

            full = os.path.join(self.path,f)

            if os.path.isdir(full):
                icon = self.style().standardIcon(QStyle.SP_DirIcon)
            else:
                icon = self.style().standardIcon(QStyle.SP_FileIcon)

            item.setIcon(icon)
            item.setText(f)

            self.list.addItem(item)

    def open_item(self,item):

        name = item.text()
        full = os.path.join(self.path,name)

        if os.path.isdir(full):
            self.path = full
            self.load_files()
        else:
            os.startfile(full)

    def go_back(self):

        parent = os.path.dirname(self.path)

        if parent:
            self.path = parent
            self.load_files()

    def delete_file(self):

        item = self.list.currentItem()

        if not item:
            return

        name = item.text()
        full = os.path.join(self.path,name)

        if os.path.isfile(full):
            os.remove(full)

        self.load_files()

    def upload_file(self):

        file,_ = QFileDialog.getOpenFileName(self,"Select file")

        if file:

            name = os.path.basename(file)
            dest = os.path.join(self.path,name)

            with open(file,"rb") as src:
                with open(dest,"wb") as dst:
                    dst.write(src.read())

        self.load_files()


app = QApplication(sys.argv)

window = IOSFileManager()
window.show()

sys.exit(app.exec_())
