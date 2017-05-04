# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainXldigestWindow(object):
    def setupUi(self, MainXldigestWindow):
        MainXldigestWindow.setObjectName("MainXldigestWindow")
        MainXldigestWindow.resize(816, 687)
        self.centralwidget = QtWidgets.QWidget(MainXldigestWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.overviewWidget = OverviewWidget(self.centralwidget)
        self.overviewWidget.setObjectName("overviewWidget")
        self.gridLayout.addWidget(self.overviewWidget, 0, 0, 1, 1)
        MainXldigestWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainXldigestWindow)
        self.statusbar.setObjectName("statusbar")
        MainXldigestWindow.setStatusBar(self.statusbar)
        self.actionTemplate_Manager = QtWidgets.QAction(MainXldigestWindow)
        self.actionTemplate_Manager.setObjectName("actionTemplate_Manager")

        self.retranslateUi(MainXldigestWindow)
        QtCore.QMetaObject.connectSlotsByName(MainXldigestWindow)

    def retranslateUi(self, MainXldigestWindow):
        _translate = QtCore.QCoreApplication.translate
        MainXldigestWindow.setWindowTitle(_translate("MainXldigestWindow", "xldigest"))
        self.actionTemplate_Manager.setText(_translate("MainXldigestWindow", "Template Manager..."))

from xldigest.widgets.overview import OverviewWidget
