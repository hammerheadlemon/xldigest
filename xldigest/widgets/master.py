"""
A Qt version of the old bcompiler master spreadsheet. Re-written for the new
age...
"""
from PyQt5 import QtWidgets, QtCore

from xldigest.database.base_queries import (
    datamap_items_in_return,
    forumulate_data_for_master_model,
    project_ids_in_returns_with_series_item_of,
    project_names_per_quarter,
    create_master_friendly_header,
    series_items,
    series_item_ids_in_returns
)


class MasterTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data_in, parent=None):
        super().__init__(parent)
        self.data_in = data_in
        self.p_names_on_pop_form = list(self.data_in[0])
        self.headers = create_master_friendly_header(
            self.p_names_on_pop_form, 1)
        self.headers.insert(0, "DMI")
        self.headers.insert(1, "Key")

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data_in)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.data_in[0])

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data_in[row][col]
            return value

    def headerData(self, section, orientation, role):
        headers = self.headers
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return headers[section]
            else:
                return section + 1

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled


class MasterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.series_label = QtWidgets.QLabel("Select Series Item")
        self.series_combo = QtWidgets.QComboBox(self)
        self.set_series_item_combo()
        self.selected_series_item = self.series_combo.itemData(0, QtCore.Qt.UserRole)
        self.series_combo.currentIndexChanged.connect(self._swap_table_slot)

        project_ids = project_ids_in_returns_with_series_item_of(
            self.selected_series_item)  # TODO to get which series_item
        # FIXME - this shit is hard-coded
        self.datamap_keys = datamap_items_in_return(1, 1)  # TODO likewise - fix hard-cde
        self.table_data = forumulate_data_for_master_model(
            self.selected_series_item, project_ids, self.datamap_keys)

        self.tv = QtWidgets.QTableView()
        self.tv.verticalHeader().hide()
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.tableModel = MasterTableModel(self.table_data, self)
        self.tv.setModel(self.proxyModel)
        self.proxyModel.setSourceModel(self.tableModel)
        self.tv.setSortingEnabled(True)
        self.tv.horizontalHeader().setStretchLastSection(False)
        col_count = self.tableModel.columnCount()
        self.tv.setColumnWidth(0, 50)
        self.tv.setColumnWidth(1, 300)
        for c in range(2, col_count):
            self.tv.setColumnWidth(c, 200)
        self.sortCaseSensitivityCheckBox = QtWidgets.QCheckBox(
            "Case sensitive sorting")
        self.filterCaseSensitivityCheckBox = QtWidgets.QCheckBox(
            "Case sensitive filter")
        self.filterPatternLineEdit = QtWidgets.QLineEdit()
        self.filterPatternLabel = QtWidgets.QLabel("Filter pattern")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)
        self.filterSyntaxCombo = QtWidgets.QComboBox()
        self.filterSyntaxCombo.addItem("Regular Expression",
                                       QtCore.QRegExp.RegExp)
        self.filterSyntaxCombo.addItem("Wildcard", QtCore.QRegExp.Wildcard)
        self.filterSyntaxCombo.addItem("Fixed string",
                                       QtCore.QRegExp.FixedString)
        self.filterSyntaxLabel = QtWidgets.QLabel("Filter syntax:")
        self.filterSyntaxLabel.setBuddy(self.filterSyntaxCombo)
        self.filterColumnCombo = QtWidgets.QComboBox()
        self.filterColumnCombo.addItem("Project 1")
        self.filterColumnLabel = QtWidgets.QLabel("Filter column:")
        self.filterColumnLabel.setBuddy(self.filterColumnCombo)


        self.filterPatternLineEdit.textChanged.connect(self.filterRegExChanged)
        self.filterSyntaxCombo.currentIndexChanged.connect(
            self.filterRegExChanged)
        self.filterColumnCombo.currentIndexChanged.connect(
            self.filterColumnChanged)
        self.filterCaseSensitivityCheckBox.toggled.connect(self.sortChanged)

        proxyGroupBox = QtWidgets.QGroupBox("Master Data")
        proxyLayout = QtWidgets.QGridLayout()
        proxyLayout.addWidget(self.series_label, 0, 1, 1, 2)
        proxyLayout.addWidget(self.series_combo, 0, 0, 1, 1)
        proxyLayout.addWidget(self.tv, 1, 0, 1, 3)
        proxyLayout.addWidget(self.filterPatternLabel, 2, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 2, 1, 1, 2)
        proxyLayout.addWidget(self.filterSyntaxLabel, 3, 0)
        proxyLayout.addWidget(self.filterSyntaxCombo, 3, 1, 1, 2)
        proxyLayout.addWidget(self.filterColumnLabel, 4, 0)
        proxyLayout.addWidget(self.filterColumnCombo, 4, 1, 1, 2)
        proxyLayout.addWidget(self.filterCaseSensitivityCheckBox, 5, 0, 1, 2)
        proxyLayout.addWidget(self.sortCaseSensitivityCheckBox, 5, 2)
        proxyGroupBox.setLayout(proxyLayout)

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(proxyGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("xldigest Master View")

        self.tv.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.filterColumnCombo.setCurrentIndex(1)

        self.filterPatternLineEdit.setText("")
        self.filterCaseSensitivityCheckBox.setChecked(False)
        self.sortCaseSensitivityCheckBox.setChecked(False)

    def _swap_table_slot(self, index):
        si = self.series_combo.itemData(index, QtCore.Qt.UserRole)
        project_ids = project_ids_in_returns_with_series_item_of(
            si)
        self.table_data = forumulate_data_for_master_model(
            si, project_ids, self.datamap_keys)
        self.tableModel = MasterTableModel(self.table_data, self)
        self.proxyModel.setSourceModel(self.tableModel)
        self.tv.setModel(self.proxyModel)

    def set_series_item_combo(self):
        for item in series_item_ids_in_returns():
            self.series_combo.addItem(item[1], item[0])

    def filterRegExChanged(self):
        syntax = QtCore.QRegExp.PatternSyntax(
            self.filterSyntaxCombo.itemData(
                self.filterSyntaxCombo.currentIndex()))
        caseSensitivity = self.filterCaseSensitivityCheckBox.isChecked()
        regex = QtCore.QRegExp(self.filterPatternLineEdit.text(),
                               caseSensitivity, syntax)
        self.proxyModel.setFilterRegExp(regex)

    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(
            self.filterColumnCombo.currentIndex())

    def sortChanged(self):
        self.proxyModel.setSortCaseSensitivity(
            self.sortCaseSensitivityCheckBox.isChecked())
