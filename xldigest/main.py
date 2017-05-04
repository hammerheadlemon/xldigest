# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_test.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!
import sys

from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore

import icons_rc

from xldigest.widgets.main_ui import Ui_MainXldigestWindow
from xldigest.widgets.base_import_wizard import BaseImportWizard
from xldigest.widgets.datamap import DatamapWindow
from xldigest.widgets.overview import OverviewWidget
from xldigest.widgets.returnswindow import ReturnsWindow
from xldigest.widgets.template_manager_window import TemplateManagerWindow
from xldigest.widgets.importreturns import ImportReturns
from xldigest.database.setup import USER_DATA_DIR


def test_db():
    if Path(USER_DATA_DIR + '/db.sqlite').is_file():
        return True
    else:
        return False


DATABASE_PRESENT = test_db()


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
        self.toolBar.addAction(QtGui.QIcon(self.overviewIcon), "Overview", self.set_overview_central)

        self.datamapIcon = QtGui.QPixmap(':/tools.png')
        self.toolBar.addAction(QtGui.QIcon(self.datamapIcon), "Datamap", self.set_datamap_central)

        self.returnsIcon = QtGui.QPixmap(':/upload.png')
        self.toolBar.addAction(QtGui.QIcon(self.returnsIcon), "Returns", self.set_returns_central)

        self.templatesIcon = QtGui.QPixmap(':/dev.png')
        self.toolBar.addAction(QtGui.QIcon(self.templatesIcon), "Templates", self.set_template_central)

        self.importIcon = QtGui.QPixmap(':/arrow-down.png')
        self.toolBar.addAction(QtGui.QIcon(self.importIcon), "Imports", self.set_import_central)

        if not DATABASE_PRESENT:
            self.overviewWidget.databasePresentLabel.setEnabled(True)
            self.overviewWidget.baseSetupButton.setEnabled(True)
            self.overviewWidget.baseSetupButton.clicked.connect(self._launch_wizard)

    def set_import_central(self):
        self.i_widget = ImportReturns()
        self.setCentralWidget(self.i_widget)

    def set_template_central(self):
        self.t_widget = TemplateManagerWindow()
        self.setCentralWidget(self.t_widget)

    def set_datamap_central(self):
        self.dm_widget = DatamapWindow()
        self.setCentralWidget(self.dm_widget)

    def set_overview_central(self):
        self.o_widget = OverviewWidget()
        self.setCentralWidget(self.o_widget)

    def set_returns_central(self):
        self.r_widget = ReturnsWindow()
        self.setCentralWidget(self.r_widget)

    def _launch_wizard(self):
        wizard = BaseImportWizard()
        if wizard.exec_():
            self.refreshUi()

    def refreshUi(self):
        pass


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
