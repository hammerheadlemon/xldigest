# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_test.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtGui, QtWidgets
from xldigest.widgets.main_test import Ui_MainXldigestWindow
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


class TableViewWidgetTest(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(TableViewWidgetTest, self).__init__(parent)
        self.setColumnCount(5)
        self.setRowCount(200)


class XldigestMainWindow(QtWidgets.QMainWindow, Ui_MainXldigestWindow):
    def __init__(self, parent=None):
        super(XldigestMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget = TableViewWidgetTest(self.tab_5)
        self.datamapConfig = DatamapTable(self.tab_2)
        self.datamapConfig.setEnabled(True)
        self.verticalLayout.addWidget(self.datamapConfig)


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
