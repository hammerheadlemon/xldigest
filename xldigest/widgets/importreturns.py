from PyQt5 import QtWidgets

from xldigest.widgets.import_returns_tab_ui import Ui_ImportManager


class ImportReturns(QtWidgets.QWidget, Ui_ImportManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
