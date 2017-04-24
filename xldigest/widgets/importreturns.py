from PyQt5 import QtWidgets

from xldigest.widgets.import_returns_tab_ui import Ui_ImportManager
from xldigest.database.setup import USER_DATA_DIR


class ImportReturns(QtWidgets.QWidget, Ui_ImportManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_return_source_files)

    def get_return_source_files(self):
        print("Launching dialog to choose source files for returns")
        self.import_returns_dir_dialog = QtWidgets.QFileDialog()
        self.import_returns_dir_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.import_returns_dir_dialog.setDirectory(USER_DATA_DIR)
        self.import_returns_dir_dialog.show()
        if self.import_returns_dir_dialog.exec():
            self.selected_files = self.import_returns_dir_dialog.selectedFiles()
            print(self.selected_files)
