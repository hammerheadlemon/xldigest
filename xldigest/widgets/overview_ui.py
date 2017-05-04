# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overview.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dataOverviewWidget(object):
    def setupUi(self, dataOverviewWidget):
        dataOverviewWidget.setObjectName("dataOverviewWidget")
        dataOverviewWidget.resize(640, 657)
        self.gridLayout_2 = QtWidgets.QGridLayout(dataOverviewWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.projectPortfolioGB = QtWidgets.QGroupBox(dataOverviewWidget)
        self.projectPortfolioGB.setObjectName("projectPortfolioGB")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.projectPortfolioGB)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableView(self.projectPortfolioGB)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.gridLayout.addWidget(self.projectPortfolioGB, 0, 0, 1, 1)
        self.databasePortfolioGB = QtWidgets.QGroupBox(dataOverviewWidget)
        self.databasePortfolioGB.setObjectName("databasePortfolioGB")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.databasePortfolioGB)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.databasePortfolioGB)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.databasePresentLabel = QtWidgets.QLabel(self.databasePortfolioGB)
        self.databasePresentLabel.setEnabled(False)
        self.databasePresentLabel.setObjectName("databasePresentLabel")
        self.verticalLayout.addWidget(self.databasePresentLabel)
        self.baseSetupButton = QtWidgets.QPushButton(self.databasePortfolioGB)
        self.baseSetupButton.setEnabled(False)
        self.baseSetupButton.setObjectName("baseSetupButton")
        self.verticalLayout.addWidget(self.baseSetupButton)
        self.gridLayout.addWidget(self.databasePortfolioGB, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(dataOverviewWidget)
        QtCore.QMetaObject.connectSlotsByName(dataOverviewWidget)

    def retranslateUi(self, dataOverviewWidget):
        _translate = QtCore.QCoreApplication.translate
        dataOverviewWidget.setWindowTitle(_translate("dataOverviewWidget", "Form"))
        self.projectPortfolioGB.setTitle(_translate("dataOverviewWidget", "Project/Portfolio List"))
        self.databasePortfolioGB.setTitle(_translate("dataOverviewWidget", "Database"))
        self.databasePresentLabel.setText(_translate("dataOverviewWidget", "No database present - please use Base Setup Wizard to initialise application"))
        self.baseSetupButton.setText(_translate("dataOverviewWidget", "Base Setup Wizard"))

