from PyQt5 import QtWidgets, QtCore, QtGui

from xldigest.widgets.import_returns_tab_ui import Ui_ImportManager
from xldigest.database.setup import USER_DATA_DIR


class ImportReturns(QtWidgets.QWidget, Ui_ImportManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.launchFileDialog.clicked.connect(self.get_return_source_files)
        self.portfolio_model = self._pop_portfolio_dropdown()
        self.comboPortfolio.setModel(self.portfolio_model)

    def get_return_source_files(self):
        print("Launching dialog to choose source files for returns")
        self.import_returns_dir_dialog = QtWidgets.QFileDialog()
        self.import_returns_dir_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.import_returns_dir_dialog.setDirectory(USER_DATA_DIR)
        self.import_returns_dir_dialog.show()
        if self.import_returns_dir_dialog.exec():
            self.selected_files = self.import_returns_dir_dialog.selectedFiles()
            print(self.selected_files)

    def _pop_portfolio_dropdown(self):
        model = QtGui.QStandardItemModel()

        items = ["Test 1", "Test 2", "Test 3"]

        for item in items:
            item_text = QtGui.QStandardItem(item)
            model.appendRow(item_text)
        return model
