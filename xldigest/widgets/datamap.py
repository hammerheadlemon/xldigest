import sys
import sqlite3

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

# from https://www.youtube.com/watch?v=2sRoLN337cs


class DatamapTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data_in=[[]], parent=None, *args):
        super(DatamapTableModel, self).__init__(parent, *args)

        self.data = data_in

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.data[0])

    def data(self, index, role):

        # we want to text to remain when we double-click it
        # otherwise, we'd lose the original data
        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            return self.data[row][col]

        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            return "{} item".format(self.data[row][0])

        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data[row][col]
            return value

        # HERE WE INCLUDE A COLOURED ICON!
#        if index.isValid() and role == QtCore.Qt.DecorationRole:
#            row = index.row()
#            col = index.column()
#            value = self.data[row][col]
#
#            # making a colour icon for a laugh
#            pixmap = QtGui.QPixmap(26, 26)
#            pixmap.fill(QtGui.QColor(233, 23, 233))
#
#            icon = QtGui.QIcon(pixmap)
#            return icon

    # we want headers for our table
    def headerData(self, section, orientation, role):

        headers = [
            "Index",
            "Key",
            "BICC Sheet",
            "BICC Cell Reference",
            "GMPP Sheet",
            "GMPP Cell Reference",
            "Verification Rule"
        ]

        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return headers[section]
            else:
                return section + 1

    # need this to make it editable, selectable and enabled
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | \
            QtCore.Qt.ItemIsSelectable

    # need this to make it editable
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            self.data[row][col] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        # this must be called before inserting rows
        # this emit signals which are handled by views
        self.beginInsertRows(
            parent, position, position + rows-1)

        # DO INSERTING HERE!
        for i in range(rows):

            default_values = [
                "Default Value" for i in range(self.columnCount(None))]

            self.data.insert(position, default_values)

        # this must be called after inserting rows
        self.endInsertRows()
        return True


def pull_all_data_from_db():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    d = list(c.execute("SELECT * FROM datamap_item"))
    c.close()
    conn.close()
    return d


class DatamapWindow(QtWidgets.QWidget):
    def __init__(self, *args):
        super(DatamapWindow, self).__init__(*args)
        self.setWindowTitle('Configure Datamaps')
        self.resize(900, 600)
        desktop = QtWidgets.QDesktopWidget().availableGeometry()
        width = (desktop.width() - self.width()) / 2
        height = (desktop.height() - self.height()) / 2
        self.move(width, height)

        # convert from tuples to list
        table_data = [list(item) for item in pull_all_data_from_db()]

        self.tv = QtWidgets.QTableView()

        self.tableModel = DatamapTableModel(table_data, self)
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.tv.setModel(self.proxyModel)
        self.proxyModel.setSourceModel(self.tableModel)
        self.tv.setSortingEnabled(True)

        self.tv.resize(900, 400)
        self.tv.horizontalHeader().setStretchLastSection(True)

        self.sortCaseSensitivityCheckBox = QtWidgets.QCheckBox(
            "Case sensitive sorting")
        self.filterCaseSensitivityCheckBox = QtWidgets.QCheckBox(
            "Case sensitive filter")

        self.filterPatternLineEdit = QtWidgets.QLineEdit()
        self.filterPatternLabel = QtWidgets.QLabel("Filter pattern")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterSyntaxCombo = QtWidgets.QComboBox()
        self.filterSyntaxCombo.addItem(
            "Regular Expression", QtCore.QRegExp.RegExp)
        self.filterSyntaxCombo.addItem(
            "Wildcard", QtCore.QRegExp.Wildcard)
        self.filterSyntaxCombo.addItem(
            "Fixed string", QtCore.QRegExp.FixedString)
        self.filterSyntaxLabel = QtWidgets.QLabel("Filter syntax:")
        self.filterSyntaxLabel.setBuddy(self.filterSyntaxCombo)

        self.filterColumnCombo = QtWidgets.QComboBox()
        self.filterColumnCombo.addItem("Index")
        self.filterColumnCombo.addItem("Key")
        self.filterColumnCombo.addItem("BICC Sheet")
        self.filterColumnCombo.addItem("BICC Cell Reference")
        self.filterColumnCombo.addItem("GMPP Sheet")
        self.filterColumnCombo.addItem("GMPP Cell Reference")
        self.filterColumnCombo.addItem("Verification Rule")
        self.filterColumnLabel = QtWidgets.QLabel("Filter column:")
        self.filterColumnLabel.setBuddy(self.filterColumnCombo)

        # SIGNALS
        self.filterPatternLineEdit.textChanged.connect(
            self.filterRegExChanged)

        self.filterSyntaxCombo.currentIndexChanged.connect(
            self.filterRegExChanged)

        self.filterColumnCombo.currentIndexChanged.connect(
            self.filterColumnChanged)

        self.filterCaseSensitivityCheckBox.toggled.connect(
            self.filterRegExChanged)

        self.sortCaseSensitivityCheckBox.toggled.connect(self.sortChanged)

        proxyGroupBox = QtWidgets.QGroupBox("Datamap Configuration")

        proxyLayout = QtWidgets.QGridLayout()
        proxyLayout.addWidget(self.tv, 0, 0, 1, 3)
        proxyLayout.addWidget(self.filterPatternLabel, 1, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1, 1, 2)
        proxyLayout.addWidget(self.filterSyntaxLabel, 2, 0)
        proxyLayout.addWidget(self.filterSyntaxCombo, 2, 1, 1, 2)
        proxyLayout.addWidget(self.filterColumnLabel, 3, 0)
        proxyLayout.addWidget(self.filterColumnCombo, 3, 1, 1, 2)
        proxyLayout.addWidget(self.filterCaseSensitivityCheckBox, 4, 0, 1, 2)
        proxyLayout.addWidget(self.sortCaseSensitivityCheckBox, 4, 2)
        proxyGroupBox.setLayout(proxyLayout)

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(proxyGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("xldigest Datamap")

        self.tv.sortByColumn(1, Qt.AscendingOrder)
        self.filterColumnCombo.setCurrentIndex(1)

        self.filterPatternLineEdit.setText("")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.sortCaseSensitivityCheckBox.setChecked(False)

    def filterRegExChanged(self):
        syntax = QtCore.QRegExp.PatternSyntax(self.filterSyntaxCombo.itemData(
            self.filterSyntaxCombo.currentIndex()))
        caseSensitivity = self.filterCaseSensitivityCheckBox.isChecked()
        regex = QtCore.QRegExp(
            self.filterPatternLineEdit.text(), caseSensitivity, syntax)
        self.proxyModel.setFilterRegExp(regex)

    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(
            self.filterColumnCombo.currentIndex())

    def sortChanged(self):
        self.proxyModel.setSortCaseSensitivity(
            self.sortCaseSensitivityCheckBox.isChecked())


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = DatamapWindow()
    w.show()
#    data = ["one", "two", "three", "four"]
#
#    listView = QtWidgets.QListView()
#    listView.show()
#
#    # model! better way to do things
#    model = QtCore.QStringListModel(data)
#
#    listView.setModel(model)
#
#    comboBox = QtWidgets.QComboBox()
#    comboBox.setModel(model)
#    comboBox.show()
#
#    listView2 = QtWidgets.QListView()
#    listView2.show()
#    listView2.setModel(model)

#    # list widget - this is not good
#    listWidget = QtWidgets.QListWidget()
#    listWidget.show()
#    listWidget.addItems(data)
#
#
#    # make the list items editable
#    count = listWidget.count()
#    for i in range(count):
#        item = listWidget.item(i)
#        print(item.flags())
#        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
#
#    comboBox = QtWidgets.QComboBox()
#    comboBox.show()
#    comboBox.addItems(data)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
