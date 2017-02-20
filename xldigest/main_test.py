# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_test.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from xldigest.widgets.main_test import Ui_MainWindow
from xldigest.widgets.datamap import DatamapTableModel


class DatamapTable(QtWidgets.QTableView):
    def __init__(self, *args):
        super(DatamapTable, self).__init__(*args)
        table_data = [["Hi", "Hi", "Hi", "Hi", "Hi", "Hi", "Hi"],
                      ["Hi", "Hi", "Hi", "Hi", "Hi", "Hi", "Hi"],
                      ["Hi", "Hi", "Hi", "Hi", "Hi", "Hi", "Hi"]]
        self.tableModel = DatamapTableModel(table_data, self)
        self.setModel(self.tableModel)
        self.setSortingEnabled(True)


def main():
    application = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.datamapConfig = DatamapTable()
    desktop = QtWidgets.QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 3
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
