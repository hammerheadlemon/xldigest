import os

from PyQt5 import QtWidgets, QtGui, QtCore

from xldigest.widgets.import_returns_tab_ui import Ui_ImportManager
from xldigest.database.setup import USER_DATA_DIR, set_up_session
from xldigest.database.models import Portfolio, Series, SeriesItem
from xldigest.database.base_queries import (
    project_names_in_portfolio, portfolio_names, series_names, series_items)

db_pth = os.path.join(USER_DATA_DIR, 'db.sqlite')
session = set_up_session(db_pth)


class ImportReturns(QtWidgets.QWidget, Ui_ImportManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.launchFileDialog.clicked.connect(self.get_return_source_files)
        self.portfolio_model = self._pop_portfolio_dropdown()
        self.comboPortfolio.setModel(self.portfolio_model)
        self.comboPortfolio.activated.connect(self._portfolio_select)
        self.series_model = self._pop_series_dropdown()
        self.comboSeries.setModel(self.series_model)
        self.comboSeries.activated.connect(self._series_select)
        self._selected_series_id = 0
        self.series_item_model = self._pop_series_item_dropdown()
        self.comboSeriesItem.setModel(self.series_item_model)
        self.comboSeriesItem.activated.connect(self._series_item_select)
        self.selectedCountLabel.setText("")

    def _make_model_data_list(self, *args):
        """
        Tiny helper method.
        """
        return list(args)

    def get_return_source_files(self):
        print("Launching dialog to choose source files for returns")
        self.import_returns_dir_dialog = QtWidgets.QFileDialog()
        self.import_returns_dir_dialog.setFileMode(
            QtWidgets.QFileDialog.ExistingFiles)
        self.import_returns_dir_dialog.setDirectory(USER_DATA_DIR)
        self.import_returns_dir_dialog.setNameFilter("Excel files (*.xlsx)")
        self.import_returns_dir_dialog.show()
        if self.import_returns_dir_dialog.exec():
            self.selected_files = self.import_returns_dir_dialog.selectedFiles()
            print(self.selected_files)
            l = []
            for sfile in self.selected_files:
                # we want to replace with section of code with a deployment of
                # QThread (https://nikolak.com/pyqt-threading-tutorial/"
                # is a decent example
                sfile = sfile.split('/')[-1]
                l.append(
                    self._make_model_data_list(sfile, "bollocks",
                                               "--Confirm Project Title--"))
            self.model_selected_returns = SelectedFilesModel(l)
            self.selectedFilesWidget.setModel(self.model_selected_returns)
            self.selectedFilesWidget.setItemDelegateForColumn(
                2, DropDownDelegate(self.selectedFilesWidget))
            self.selectedFilesWidget.setEditTriggers(
                QtWidgets.QAbstractItemView.CurrentChanged)
            self.selectedFilesWidget.horizontalHeader().setStretchLastSection(
                True)
            print(l)
        try:
            self.selectedCountLabel.setText(
                "{} files selected".format(len(self.selected_files)))
        except AttributeError:
            print("No files selected")

    def _portfolio_select(self, index):
        print("got that portfolio sig: {}".format(index))

    def _series_select(self, index):
        idx = self.series_model.index(0, index)
        try:
            self._selected_series_id = session.query(Series.id).filter(
                Series.name == self.series_model.data(idx, QtCore.Qt.DisplayRole)).all()[0][0]
        except IndexError:
            self._selected_series_id = index + 1
            print("There are no SeriesItems that related to Series: {}".format(
                self._selected_series_id))
            self.comboSeriesItem.setModel(QtGui.QStandardItemModel())
            self.comboSeriesItem.clear()
        print("got that series sig: {} - index in db: {}".format(
            self.series_model.data(idx, QtCore.Qt.DisplayRole), self._selected_series_id))
        self.series_item_model = self._pop_series_item_dropdown()
        self.comboSeriesItem.setModel(self.series_item_model)

    def _series_item_select(self, index):
        print("got that series item sig: {}".format(index))

    def _pop_portfolio_dropdown(self):
        self.portfolio_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = portfolio_names()

        for item in items:
            item_text = QtGui.QStandardItem(item)
            self.portfolio_model.appendRow(item_text)
        return self.portfolio_model

    def _pop_series_dropdown(self):
        self.series_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = series_names()

        for item in items:
            item_text = QtGui.QStandardItem(item)
            self.series_model.appendRow(item_text)
        return self.series_model

    def _pop_series_item_dropdown(self):
        self.series_item_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = series_items(self._selected_series_id)

        for item in items:
            item_text = QtGui.QStandardItem(item)
            self.series_item_model.appendRow(item_text)
        return self.series_item_model


class DropDownDelegate(QtWidgets.QStyledItemDelegate):
    """
    Used to enable selection of project titles from the database, to associate
    them with the return file we want to import.
    """

    def __init__(self, parent):
        super().__init__(parent)

    # Here we create the editor we want to impose upon the cell in the TableView
    # - in this case it is a combo box.
    def createEditor(self, parent, option, index):
        if index.column() == 2:
            combo = QtWidgets.QComboBox(parent)
            li = sorted(
                project_names_in_portfolio(1))  # hard-coded portfolio just now
            combo.addItems(li)
            combo.currentIndexChanged.connect(self.currentIndexChangedSlot)
            return combo

    # what do we do when combo selection is changed. This requests that we commit
    # the data to the model.
    def currentIndexChangedSlot(self):
        self.commitData.emit(self.sender())

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class SelectedFilesModel(QtCore.QAbstractTableModel):
    """
    Status of selected return files. Needed so that we can match up what we're
    intending to import with whats in the database. We don't want duplicates.
    """

    def __init__(self, data_in, parent=None, *args):
        super().__init__(parent)
        self.data_in = data_in

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data_in)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.data_in[0])

    def headerData(self, section, orientation, role):
        headers = ["File Name", "Status", "Project Name"]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return headers[section]
            else:
                return section + 1

    def flags(self, index):
        if (index.column() == 2):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data_in[row][col]
            return value

    # we need this because the model has to accept a change in data from
    # the ComboDelegate. Without overriding this method, we can change the value
    # in the combo, but the value is not retained in the model
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print("setData", index.row(), index.column(), value)
        self.data_in[index.row()][index.column()] = value
