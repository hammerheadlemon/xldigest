from PyQt5 import QtWidgets, QtGui, QtCore

from xldigest.widgets.import_returns_tab_ui import Ui_ImportManager
from xldigest.database.setup import USER_DATA_DIR


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
        self.import_returns_dir_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
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
                l.append(self._make_model_data_list(sfile, "bollocks", "Project"))
            self.model_selected_returns = SelectedFilesModel(l)
            self.selectedFilesWidget.setItemDelegateForColumn(2, DropDownDelegate(self))
            self.selectedFilesWidget.setModel(self.model_selected_returns)
            self.selectedFilesWidget.horizontalHeader().setStretchLastSection(True)
            print(l)
        self.selectedCountLabel.setText("{} files selected".format(len(self.selected_files)))

    def _portfolio_select(self, index):
        print("got that portfolio sig: {}".format(index))

    def _series_select(self, index):
        print("got that series sig: {}".format(index))

    def _series_item_select(self, index):
        print("got that series item sig: {}".format(index))

    def _pop_portfolio_dropdown(self):
        model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = ["Portfolio 1", "Portfolio 2", "Portfolio 3"]

        for item in items:
            item_text = QtGui.QStandardItem(item)
            model.appendRow(item_text)
        return model

    def _pop_series_dropdown(self):
        model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = ["Series 1", "Series 2", "Series 3"]

        for item in items:
            item_text = QtGui.QStandardItem(item)
            model.appendRow(item_text)
        return model

    def _pop_series_item_dropdown(self):
        model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = ["Series Item 1", "Series Item 2", "Series Item 3"]

        for item in items:
            item_text = QtGui.QStandardItem(item)
            model.appendRow(item_text)
        return model


class DropDownDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        combo = QtWidgets.QComboBox(parent)
        li = []
        li.append("Boo")
        li.append("Smersh")
        li.append("Conkers")
        combo.addItems(li)
        combo.currentIndexChanged.connect(self.currentIndexChangedSlot)
        return combo

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
        headers = [
            "File Name",
            "Status",
            "Project Name"
        ]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return headers[section]
            else:
                return section + 1

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data_in[row][col]
            return value
