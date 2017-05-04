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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.overviewWidget = OverviewWidget(self.tab)
        self.overviewWidget.setObjectName("overviewWidget")
        self.horizontalLayout.addWidget(self.overviewWidget)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = DatamapWindow(self.tab_2)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.returnsWidget = ReturnsWindow(self.tab_5)
        self.returnsWidget.setObjectName("returnsWidget")
        self.horizontalLayout_5.addWidget(self.returnsWidget)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.templateManagerWidget = TemplateManagerWindow(self.tab_3)
        self.templateManagerWidget.setObjectName("templateManagerWidget")
        self.horizontalLayout_6.addWidget(self.templateManagerWidget)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout.setObjectName("gridLayout")
        self.importReturns = ImportReturns(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importReturns.sizePolicy().hasHeightForWidth())
        self.importReturns.setSizePolicy(sizePolicy)
        self.importReturns.setObjectName("importReturns")
        self.gridLayout.addWidget(self.importReturns, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.finishButton = QtWidgets.QPushButton(self.centralwidget)
        self.finishButton.setObjectName("finishButton")
        self.horizontalLayout_3.addWidget(self.finishButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        MainXldigestWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainXldigestWindow)
        self.statusbar.setObjectName("statusbar")
        MainXldigestWindow.setStatusBar(self.statusbar)
        self.actionTemplate_Manager = QtWidgets.QAction(MainXldigestWindow)
        self.actionTemplate_Manager.setObjectName("actionTemplate_Manager")

        self.retranslateUi(MainXldigestWindow)
        self.tabWidget.setCurrentIndex(0)
        self.finishButton.clicked.connect(MainXldigestWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainXldigestWindow)

    def retranslateUi(self, MainXldigestWindow):
        _translate = QtCore.QCoreApplication.translate
        MainXldigestWindow.setWindowTitle(_translate("MainXldigestWindow", "xldigest"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainXldigestWindow", "Project Summary"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainXldigestWindow", "Datamap"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainXldigestWindow", "Returns"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainXldigestWindow", "Templates"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainXldigestWindow", "Import Returns"))
        self.finishButton.setText(_translate("MainXldigestWindow", "Finish"))
        self.actionTemplate_Manager.setText(_translate("MainXldigestWindow", "Template Manager..."))

from xldigest.widgets.datamap import DatamapWindow
from xldigest.widgets.importreturns import ImportReturns
from xldigest.widgets.overview import OverviewWidget
from xldigest.widgets.returnswindow import ReturnsWindow
from xldigest.widgets.template_manager_window import TemplateManagerWindow
