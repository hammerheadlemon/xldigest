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
        ImportManager.resize(498, 483)
        self.widget = QtWidgets.QWidget(ImportManager)
        self.widget.setGeometry(QtCore.QRect(13, 13, 210, 116))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.launchFileDialog = QtWidgets.QPushButton(self.widget)
        self.launchFileDialog.setObjectName("launchFileDialog")
        self.horizontalLayout_4.addWidget(self.launchFileDialog)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.comboPortfolio = QtWidgets.QComboBox(self.widget)
        self.comboPortfolio.setObjectName("comboPortfolio")
        self.horizontalLayout.addWidget(self.comboPortfolio)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.comboSeries = QtWidgets.QComboBox(self.widget)
        self.comboSeries.setObjectName("comboSeries")
        self.horizontalLayout_2.addWidget(self.comboSeries)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.comboSeriesItem = QtWidgets.QComboBox(self.widget)
        self.comboSeriesItem.setObjectName("comboSeriesItem")
        self.horizontalLayout_3.addWidget(self.comboSeriesItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.widget1 = QtWidgets.QWidget(ImportManager)
        self.widget1.setGeometry(QtCore.QRect(10, 140, 481, 261))
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.selectedCountLabel = QtWidgets.QLabel(self.widget1)
        self.selectedCountLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selectedCountLabel.setObjectName("selectedCountLabel")
        self.gridLayout.addWidget(self.selectedCountLabel, 2, 1, 1, 1)
        self.selectedFilesWidget = QtWidgets.QTableView(self.widget1)
        self.selectedFilesWidget.setObjectName("selectedFilesWidget")
        self.gridLayout.addWidget(self.selectedFilesWidget, 1, 0, 1, 2)

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
        self.label.setText(_translate("ImportManager", "Files selected for import:"))
        self.selectedCountLabel.setText(_translate("ImportManager", "TextLabel"))

