from PyQt5 import QtCore, QtWidgets

from xldigest.widgets.template_manager_ui import Ui_TemplateManager


class TemplateManagerWindow(QtWidgets.QWidget, Ui_TemplateManager):
    def __init__(self, parent=None):
        super(TemplateManagerWindow, self).__init__(parent)
        self.setupUi(self)
