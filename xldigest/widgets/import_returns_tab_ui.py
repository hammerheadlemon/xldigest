# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_designer_ui/import_returns.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportManager(object):
    def setupUi(self, ImportManager):
        ImportManager.setObjectName("ImportManager")
        ImportManager.resize(669, 598)
        self.gridLayout_3 = QtWidgets.QGridLayout(ImportManager)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(ImportManager)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.launchFileDialog = QtWidgets.QPushButton(ImportManager)
        self.launchFileDialog.setObjectName("launchFileDialog")
        self.horizontalLayout_4.addWidget(self.launchFileDialog)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(ImportManager)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.comboPortfolio = QtWidgets.QComboBox(ImportManager)
        self.comboPortfolio.setObjectName("comboPortfolio")
        self.horizontalLayout.addWidget(self.comboPortfolio)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(ImportManager)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.comboSeries = QtWidgets.QComboBox(ImportManager)
        self.comboSeries.setObjectName("comboSeries")
        self.horizontalLayout_2.addWidget(self.comboSeries)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(ImportManager)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.comboSeriesItem = QtWidgets.QComboBox(ImportManager)
        self.comboSeriesItem.setObjectName("comboSeriesItem")
        self.horizontalLayout_3.addWidget(self.comboSeriesItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ImportManager)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.selectedFilesWidget = QtWidgets.QTableView(ImportManager)
        self.selectedFilesWidget.setObjectName("selectedFilesWidget")
        self.gridLayout.addWidget(self.selectedFilesWidget, 1, 0, 1, 1)
        self.selectedCountLabel = QtWidgets.QLabel(ImportManager)
        self.selectedCountLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selectedCountLabel.setObjectName("selectedCountLabel")
        self.gridLayout.addWidget(self.selectedCountLabel, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(ImportManager)
        QtCore.QMetaObject.connectSlotsByName(ImportManager)

    def retranslateUi(self, ImportManager):
        _translate = QtCore.QCoreApplication.translate
        ImportManager.setWindowTitle(_translate("ImportManager", "Form"))
        self.label_2.setText(_translate("ImportManager", "1. Select source files"))
        self.launchFileDialog.setText(_translate("ImportManager", "Choose Files to Import"))
        self.label_4.setText(_translate("ImportManager", "2. Select Portfolio"))
        self.label_5.setText(_translate("ImportManager", "3. Select Series"))
        self.label_6.setText(_translate("ImportManager", "4. Select Series Item"))
        self.label.setText(_translate("ImportManager", "Files selected for import:"))
        self.selectedCountLabel.setText(_translate("ImportManager", "TextLabel"))

