# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'returns_tab.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReturnsUI(object):
    def setupUi(self, ReturnsUI):
        ReturnsUI.setObjectName("ReturnsUI")
        ReturnsUI.resize(530, 210)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ReturnsUI)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(ReturnsUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.selectionTree = QtWidgets.QTreeView(self.splitter)
        self.selectionTree.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.selectionTree.setAlternatingRowColors(True)
        self.selectionTree.setSortingEnabled(True)
        self.selectionTree.setObjectName("selectionTree")
        self.returnsTable = QtWidgets.QTableView(self.splitter)
        self.returnsTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.returnsTable.setAlternatingRowColors(True)
        self.returnsTable.setSortingEnabled(True)
        self.returnsTable.setObjectName("returnsTable")
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(ReturnsUI)
        QtCore.QMetaObject.connectSlotsByName(ReturnsUI)

    def retranslateUi(self, ReturnsUI):
        _translate = QtCore.QCoreApplication.translate
        ReturnsUI.setWindowTitle(_translate("ReturnsUI", "Form"))

