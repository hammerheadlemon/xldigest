# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template_manager.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TemplateManager(object):
    def setupUi(self, TemplateManager):
        TemplateManager.setObjectName("TemplateManager")
        TemplateManager.resize(400, 161)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(TemplateManager)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableView(TemplateManager)
        self.tableView.setFrameShape(QtWidgets.QFrame.VLine)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.importButton = QtWidgets.QPushButton(TemplateManager)
        self.importButton.setObjectName("importButton")
        self.horizontalLayout.addWidget(self.importButton)
        self.editButton = QtWidgets.QPushButton(TemplateManager)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        self.deleteButton = QtWidgets.QPushButton(TemplateManager)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(TemplateManager)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.retranslateUi(TemplateManager)
        QtCore.QMetaObject.connectSlotsByName(TemplateManager)

    def retranslateUi(self, TemplateManager):
        _translate = QtCore.QCoreApplication.translate
        TemplateManager.setWindowTitle(_translate("TemplateManager", "Template Manager"))
        self.importButton.setText(_translate("TemplateManager", "Import Template"))
        self.editButton.setText(_translate("TemplateManager", "Edit Template"))
        self.deleteButton.setText(_translate("TemplateManager", "Delete Template"))

