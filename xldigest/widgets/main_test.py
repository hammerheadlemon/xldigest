# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_test.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainXldigestWindow(object):
    def setupUi(self, MainXldigestWindow):
        MainXldigestWindow.setObjectName("MainXldigestWindow")
        MainXldigestWindow.resize(665, 480)
        self.centralwidget = QtWidgets.QWidget(MainXldigestWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(19, 19, 631, 371))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectSummary = QtWidgets.QTableView(self.tab)
        self.projectSummary.setObjectName("projectSummary")
        self.projectSummary.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.projectSummary)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.datamapConfig = QtWidgets.QTableView(self.tab_2)
        self.datamapConfig.setEnabled(True)
        self.datamapConfig.setObjectName("datamapConfig")
        self.verticalLayout.addWidget(self.datamapConfig)
        self.pushButton = QtWidgets.QPushButton(self.tab_2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout_5.addWidget(self.tableWidget)
        self.tabWidget.addTab(self.tab_5, "")
        MainXldigestWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainXldigestWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 665, 19))
        self.menubar.setObjectName("menubar")
        MainXldigestWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainXldigestWindow)
        self.statusbar.setObjectName("statusbar")
        MainXldigestWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainXldigestWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainXldigestWindow)

    def retranslateUi(self, MainXldigestWindow):
        _translate = QtCore.QCoreApplication.translate
        MainXldigestWindow.setWindowTitle(_translate("MainXldigestWindow", "xldigest"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainXldigestWindow", "Project Summary"))
        self.pushButton.setText(_translate("MainXldigestWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainXldigestWindow", "Datamap"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainXldigestWindow", "Returns"))

