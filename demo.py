import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QFileSystemModel, QVBoxLayout, QPushButton, QStyledItemDelegate
from PyQt5.QtCore import QModelIndex, QSize, QRect
import subprocess

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttonSize = QSize(80, 20)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.data(QFileSystemModel.FilePathRole).endswith('.ppt') or index.data(QFileSystemModel.FilePathRole).endswith('.pptx'):
            rect = option.rect
            buttonRect = QRect(rect.right() - self.buttonSize.width(), rect.top()+30, self.buttonSize.width(), rect.height())
            button = QPushButton('Open', option.widget)
            button.setGeometry(buttonRect)
            button.clicked.connect(lambda: self.open_powerpoint(index))
            button.show()

    def open_powerpoint(self, index):
        file_path = index.data(QFileSystemModel.FilePathRole)
        subprocess.Popen(['start', 'powerpnt', file_path], shell=True)

class SmartPPT(QWidget):
    def __init__(self, dir_path):
        super().__init__()

        appWidth = 1000
        appHeight = 500

        self.setWindowTitle('Smart PPT')
        self.setGeometry(300, 300, appWidth, appHeight)

        self.model = QFileSystemModel()
        self.model.setRootPath(dir_path)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dir_path))
        self.tree.setColumnWidth(0, 300)
        self.tree.setAlternatingRowColors(True)
        self.tree.setItemDelegateForColumn(3, ButtonDelegate())

        layout = QVBoxLayout()
        layout.addWidget(self.tree)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dirPath = 'C:\\VS Code Projects\\SGP-IV\\SGP4\\Test'
    demo = SmartPPT(dirPath)
    demo.show()
    sys.exit(app.exec_())
