# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_returns.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportManager(object):
    def setupUi(self, ImportManager):
        ImportManager.setObjectName("ImportManager")
        ImportManager.resize(400, 314)
        self.layoutWidget = QtWidgets.QWidget(ImportManager)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 231))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.launchFileDialog = QtWidgets.QPushButton(self.layoutWidget)
        self.launchFileDialog.setObjectName("launchFileDialog")
        self.horizontalLayout_4.addWidget(self.launchFileDialog)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.comboPortfolio = QtWidgets.QComboBox(self.layoutWidget)
        self.comboPortfolio.setObjectName("comboPortfolio")
        self.horizontalLayout.addWidget(self.comboPortfolio)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.comboSeries = QtWidgets.QComboBox(self.layoutWidget)
        self.comboSeries.setObjectName("comboSeries")
        self.horizontalLayout_2.addWidget(self.comboSeries)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.comboSeriesItem = QtWidgets.QComboBox(self.layoutWidget)
        self.comboSeriesItem.setObjectName("comboSeriesItem")
        self.horizontalLayout_3.addWidget(self.comboSeriesItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(ImportManager)
        QtCore.QMetaObject.connectSlotsByName(ImportManager)

    def retranslateUi(self, ImportManager):
        _translate = QtCore.QCoreApplication.translate
        ImportManager.setWindowTitle(_translate("ImportManager", "Form"))
        self.label_2.setText(_translate("ImportManager", "1. Select source folder"))
        self.launchFileDialog.setText(_translate("ImportManager", "PushButton"))
        self.label_4.setText(_translate("ImportManager", "2. Select Portfolio"))
        self.label_5.setText(_translate("ImportManager", "3. Select Series"))
        self.label_6.setText(_translate("ImportManager", "4. Select Series Item"))

