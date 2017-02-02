import sys
import sqlite3

from PyQt5 import QtCore, QtWidgets

# from https://www.youtube.com/watch?v=2sRoLN337cs


class DropDownModel(QtCore.QAbstractListModel):
    def __init__(self, data_in, parent=None, *args):
        super(DropDownModel, self).__init__(parent, *args)

        self.data = data_in

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            return self.data[row]

        # making sure we don't remove the test completely when we edit
        # before pressing enter
        if role == QtCore.Qt.EditRole:
            row = index.row()
            return self.data[row]

    # need this to make it editable
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | \
            QtCore.Qt.ItemIsSelectable

    # need this to make it editable
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            self.data[row] = value
            # send the signal so we automatically update
            self.dataChanged.emit(index, index)
            return True
        return False

    # INSERTING and REMOVING
    # explained in https://www.youtube.com/watch?v=EmYby3BB3Kk&t=57s
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        # this must be called before inserting rows
        # this emit signals which are handled by views
        self.beginInsertRows(
            parent, position, position + rows-1)

        # DO INSERTING HERE!
        for i in range(rows):
            self.data.insert(position, "Default Value")

        # this must be called after inserting rows
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        # this must be called before removing rows
        # this emit signals which are handled by views
        self.beginRemoveRows(
            parent, position, position + rows-1)

        # REMOVE ROWS HERE!
        for i in range(rows):
            self.data.remove(self.data[position])

        # this must be called after inserting rows
        self.endRemoveRows()
        return True


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
    d = list(c.execute("SELECT * FROM datamap"))
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
        # create objects

        # convert from tuples to list
        table_data = [list(item) for item in pull_all_data_from_db()]

        # practicing the dropdown text
        dropdown_data = ["One", "Two", "Three"]

        tableModel = DatamapTableModel(table_data, self)
        tv = QtWidgets.QTableView()
        tv.setModel(tableModel)
#       tv.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tv.horizontalHeader().setStretchLastSection(True)

        # creating a combox with the dropdown_data in it
        dropdownModel = DropDownModel(dropdown_data)
        comboBox = QtWidgets.QComboBox()
        comboBox.setModel(dropdownModel)

        # if we want to insert rows
        # dropdownModel.insertRows(2, 5)

        # if we want to remove rows
        dropdownModel.removeRows(1, 1)

        # we will create a simple list view of the model too
        listView = QtWidgets.QListView()
        listView.resize(100, 100)
        listView.setModel(dropdownModel)

        # layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(tv)
        self.layout.addWidget(comboBox)
        self.layout.addWidget(listView)
        self.setLayout(self.layout)


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
