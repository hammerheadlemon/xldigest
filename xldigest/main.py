# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_test.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from xldigest.widgets.main_ui import Ui_MainXldigestWindow
from xldigest.widgets.template_manager_window import TemplateManagerWindow


class XldigestMainWindow(QtWidgets.QMainWindow, Ui_MainXldigestWindow):
    def __init__(self, parent=None):
        super(XldigestMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.toolBar = QtWidgets.QToolBar("Main Toolbar", parent=self)
        self.toolBar.setIconSize(QtCore.QSize(64, 64))
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.overviewIcon = QtGui.QPixmap('/home/lemon/Downloads/icons_tmp/circle-icons/one-color/png/64px/play.png')
        self.toolBar.addAction(QtGui.QIcon(self.overviewIcon), "Overview")

        self.datamapIcon = QtGui.QPixmap('/home/lemon/Downloads/icons_tmp/circle-icons/one-color/png/64px/tools.png')
        self.toolBar.addAction(QtGui.QIcon(self.datamapIcon), "Datamaps")

        self.returnsIcon = QtGui.QPixmap('/home/lemon/Downloads/icons_tmp/circle-icons/one-color/png/64px/upload.png')
        self.toolBar.addAction(QtGui.QIcon(self.returnsIcon), "Returns")

        self.templatesIcon = QtGui.QPixmap('/home/lemon/Downloads/icons_tmp/circle-icons/one-color/png/64px/dev.png')
        self.toolBar.addAction(QtGui.QIcon(self.templatesIcon), "Templates")

        self.importIcon = QtGui.QPixmap('/home/lemon/Downloads/icons_tmp/circle-icons/one-color/png/64px/arrow-down.png')
        self.toolBar.addAction(QtGui.QIcon(self.importIcon), "Imports")

        self.actionTemplate_Manager.triggered.connect(
            self._openTemplateManagerWindow_slot)

    def _openTemplateManagerWindow_slot(self):
        self.templateManagerWindow = TemplateManagerWindow()
        self.templateManagerWindow.show()


def main():
    application = QtWidgets.QApplication(sys.argv)
    window = XldigestMainWindow()
    desktop = QtWidgets.QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 3
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
