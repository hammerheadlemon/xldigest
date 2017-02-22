from PyQt5 import QtWidgets

from xldigest.widgets.returns_tab_ui import Ui_ReturnsUI


class ReturnsWindow(QtWidgets.QWidget, Ui_ReturnsUI):
    def __init__(self, parent=None):
        super(ReturnsWindow, self).__init__(parent)
        self.setupUi(self)
