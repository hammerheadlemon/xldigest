import sys

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp, QDate
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QWidget, QTreeView, QGroupBox,
                             QVBoxLayout, QCheckBox, QLineEdit, QLabel,
                             QComboBox, QGridLayout)


def addMail(model, key, sheet, cellref, date):
    model.insertRow(0)
    model.setData(model.index(0, 0), key)
    model.setData(model.index(0, 1), sheet)
    model.setData(model.index(0, 2), cellref)
    model.setData(model.index(0, 3), date)


def createMailModel(parent=None):

    model = QStandardItemModel(0, 3, parent)
    model.setHeaderData(0, Qt.Horizontal, "Key")
    model.setHeaderData(1, Qt.Horizontal, "Sheet")
    model.setHeaderData(2, Qt.Horizontal, "Cell Reference")
    model.setHeaderData(3, Qt.Horizontal, "Date")

    addMail(model, "Project/Programme Name", "Summary", "B3",
            QDate(2010, 8, 2))
    addMail(model, "SRO Sign-Off", "Summary", "C4", QDate(2012, 12, 2))
    addMail(model, "SRO RAG Assessment", "Finance", "G212", QDate(2010, 2, 2))
    addMail(model, "Milestone 1", "Milestones", "C23", QDate(2014, 1, 21))

    return model


class FilterWindow(QWidget):
    def __init__(self):
        super(FilterWindow, self).__init__()
        self.proxyModel = QSortFilterProxyModel()

        self.proxyView = QTreeView()
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)
        self.proxyView.setSortingEnabled(True)

        self.sortCaseSensitivityCheckBox = QCheckBox("Case sensitive sorting")
        self.filterCaseSensitivityCheckBox = QCheckBox("Case sensitive filter")

        self.filterPatternLineEdit = QLineEdit()
        self.filterPatternLabel = QLabel("Filter pattern")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxCombo = QComboBox()
        self.filterSyntaxCombo.addItem("Regular Expression", QRegExp.RegExp)
        self.filterSyntaxCombo.addItem("Wildcard", QRegExp.Wildcard)
        self.filterSyntaxCombo.addItem("Fixed string", QRegExp.FixedString)
        self.filterSyntaxLabel = QLabel("Filter syntax:")
        self.filterSyntaxLabel.setBuddy(self.filterSyntaxCombo)

        self.filterColumnCombo = QComboBox()
        self.filterColumnCombo.addItem("Key")
        self.filterColumnCombo.addItem("Sheet")
        self.filterColumnCombo.addItem("Cell Reference")
        self.filterColumnCombo.addItem("Date")
        self.filterColumnLabel = QLabel("Filter column:")
        self.filterColumnLabel.setBuddy(self.filterColumnCombo)

        # SIGNALS
        self.filterPatternLineEdit.textChanged.connect(self.filterRegExChanged)

        self.filterSyntaxCombo.currentIndexChanged.connect(
            self.filterRegExChanged)

        self.filterColumnCombo.currentIndexChanged.connect(
            self.filterColumnChanged)

        self.filterCaseSensitivityCheckBox.toggled.connect(
            self.filterRegExChanged)

        self.sortCaseSensitivityCheckBox.toggled.connect(self.sortChanged)

        self.proxyGroupBox = QGroupBox("Sorted Filtered Model")

        self.proxyLayout = QGridLayout()
        self.proxyLayout.addWidget(self.proxyView, 0, 0, 1, 3)
        self.proxyLayout.addWidget(self.filterPatternLabel, 1, 0)
        self.proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1, 1, 2)
        self.proxyLayout.addWidget(self.filterSyntaxLabel, 2, 0)
        self.proxyLayout.addWidget(self.filterSyntaxCombo, 2, 1, 1, 2)
        self.proxyLayout.addWidget(self.filterColumnLabel, 3, 0)
        self.proxyLayout.addWidget(self.filterColumnCombo, 3, 1, 1, 2)
        self.proxyLayout.addWidget(self.filterCaseSensitivityCheckBox, 4, 0, 1,
                                   2)
        self.proxyLayout.addWidget(self.sortCaseSensitivityCheckBox, 4, 2)
        self.proxyGroupBox.setLayout(self.proxyLayout)

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.proxyGroupBox)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Basic Sort/Filter Model")
        self.resize(500, 450)

        self.proxyView.sortByColumn(1, Qt.AscendingOrder)
        self.filterColumnCombo.setCurrentIndex(1)

        self.filterPatternLineEdit.setText("")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.sortCaseSensitivityCheckBox.setChecked(False)

    def setSourceModel(self, model):
        self.proxyModel.setSourceModel(model)

    def filterRegExChanged(self):
        syntax = QRegExp.PatternSyntax(
            self.filterSyntaxCombo.itemData(
                self.filterSyntaxCombo.currentIndex()))
        caseSensitivity = self.filterCaseSensitivityCheckBox.isChecked()
        regex = QRegExp(self.filterPatternLineEdit.text(), caseSensitivity,
                        syntax)
        self.proxyModel.setFilterRegExp(regex)

    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(
            self.filterColumnCombo.currentIndex())

    def sortChanged(self):
        self.proxyModel.setSortCaseSensitivity(
            self.sortCaseSensitivityCheckBox.isChecked())


def main():
    application = QApplication(sys.argv)
    window = FilterWindow()
    window.setSourceModel(createMailModel(window))
    window.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
