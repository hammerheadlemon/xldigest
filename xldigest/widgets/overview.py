from PyQt5 import QtWidgets

from xldigest.widgets.overview_ui import Ui_dataOverviewWidget


class OverviewWidget(QtWidgets.QWidget, Ui_dataOverviewWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
