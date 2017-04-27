# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_test.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtWidgets, QtGui, QtCore

import icons_rc

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

        self.overviewIcon = QtGui.QPixmap(':/play.png')
        self.toolBar.addAction(QtGui.QIcon(self.overviewIcon), "Overview")

        self.datamapIcon = QtGui.QPixmap(':/tools.png')
        self.toolBar.addAction(QtGui.QIcon(self.datamapIcon), "Datamap")

        self.returnsIcon = QtGui.QPixmap(':/upload.png')
        self.toolBar.addAction(QtGui.QIcon(self.returnsIcon), "Returns")

        self.templatesIcon = QtGui.QPixmap(':/dev.png')
        self.toolBar.addAction(QtGui.QIcon(self.templatesIcon), "Templates")

        self.importIcon = QtGui.QPixmap(':/arrow-down.png')
        self.toolBar.addAction(QtGui.QIcon(self.importIcon), "Imports")


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
