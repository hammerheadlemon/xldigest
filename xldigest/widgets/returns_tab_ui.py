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
        ReturnsUI.resize(1125, 733)
        self.widget = QtWidgets.QWidget(ReturnsUI)
        self.widget.setGeometry(QtCore.QRect(10, 40, 1101, 681))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.seletionTree = QtWidgets.QTreeView(self.widget)
        self.seletionTree.setMaximumSize(QtCore.QSize(300, 16777215))
        self.seletionTree.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.seletionTree.setSortingEnabled(True)
        self.seletionTree.setObjectName("seletionTree")
        self.horizontalLayout.addWidget(self.seletionTree)
        self.returnsTable = QtWidgets.QTableView(self.widget)
        self.returnsTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.returnsTable.setObjectName("returnsTable")
        self.horizontalLayout.addWidget(self.returnsTable)

        self.retranslateUi(ReturnsUI)
        QtCore.QMetaObject.connectSlotsByName(ReturnsUI)

    def retranslateUi(self, ReturnsUI):
        _translate = QtCore.QCoreApplication.translate
        ReturnsUI.setWindowTitle(_translate("ReturnsUI", "Form"))

