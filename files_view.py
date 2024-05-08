import subprocess
import sys

from PyQt5.QtCore import QModelIndex, QRect, QSize
from PyQt5.QtWidgets import (QApplication, QFileSystemModel, QPushButton,
                             QStackedWidget, QStyledItemDelegate, QTreeView,
                             QVBoxLayout, QWidget)

from smart_presentation import SmartPresentation
from whiteboard_ui import WhiteBoardUI


class FilesViewUI(QWidget):
    def __init__(self,path) -> None:
        super().__init__()
        self.dir_path = path
        self.flag = 0
        self.initUI()
        pass

    def initUI(self):
        appWidth = 1000
        appHeight = 500

        self.setWindowTitle('Smart PPT')
        self.setGeometry(300, 300, appWidth, appHeight)

        self.model = QFileSystemModel()
        self.model.setRootPath(self.dir_path)
        self.model.setNameFilters(["*.pptx"])

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.dir_path))
        self.tree.setColumnWidth(0, 300)
        self.tree.setAlternatingRowColors(True)

        self.tree.doubleClicked.connect(self.openPresentation)

        layout = QVBoxLayout()
        layout.addWidget(self.tree)

        self.setLayout(layout)
        pass

    def openPresentation(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        final_path = file_path.replace('/',"\\\\")

        print(f"Clicked item: {final_path}")
        self.flag = 1

        # smp = SmartPresentation()
        # smp.initPresentation(final_path)

        pass
    pass


class FilesView(QWidget):

    dir_path = str()

    def __init__(self,path):
        super().__init__()

        self.dir_path = path
        # self.files_view_ui = FilesViewUI(path)
        # self.files_view_ui.setParent(self)
        self.wb = WhiteBoardUI()
        self.initUI()
        pass


    def initUI(self):

        self.model = QFileSystemModel()
        self.model.setRootPath(self.dir_path)
        self.model.setNameFilters(["*.pptx"])

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.dir_path))
        self.tree.setColumnWidth(0, 300)
        self.tree.setAlternatingRowColors(True)

        self.tree.doubleClicked.connect(self.openPresentation)

        # self.layout1 = QVBoxLayout()
        # self.layout1.addWidget(self.tree)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.tree)
        self.stacked_widget.addWidget(self.wb)
        self.stacked_widget.setCurrentIndex(0)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        pass

    def updateUI(self, path):
        self.dir_path = path

        self.model = QFileSystemModel()
        self.model.setRootPath(self.dir_path)
        self.model.setNameFilters(["*.pptx"])

        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.dir_path))
        self.tree.setColumnWidth(0, 300)
        self.tree.setAlternatingRowColors(True)

        pass

    def openPresentation(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        final_path = file_path.replace('/',"\\\\")

        print(f"Clicked item: {final_path}")

        # smp = SmartPresentation()
        # smp.initPresentation(final_path)

        self.stacked_widget.setCurrentIndex(1)
        self.wb.ppts(final_path)
        pass
    pass








if __name__ == '__main__':
    app = QApplication(sys.argv)
    dirPath = 'C:\\Users\\yashu\\Desktop\\SGP_4\\SGP4\\Test'
    demo = FilesView(dirPath)
    demo.show()
    sys.exit(app.exec_())
