import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QApplication, QWidget, QTreeView, QFileSystemModel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QModelIndex
import subprocess

class SmartPPT(QWidget):
    def __init__(self, dir_path):
        super().__init__()

        appWidth = 1000
        appHeight = 500

        self.setWindowTitle('Smart PPT')
        self.setGeometry(300,300,appWidth,appHeight)

        self.model = QFileSystemModel()
        self.model.setRootPath(dir_path)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dirPath))
        self.tree.setColumnWidth(0,300)
        self.tree.setAlternatingRowColors(True)


        layout = QVBoxLayout()
        layout.addWidget(self.tree)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dirPath = r'C:\\VS Code Projects\\SGP-IV\\SGP4\\Test'
    demo = SmartPPT(dirPath)
    demo.show()
    sys.exit(app.exec_())
