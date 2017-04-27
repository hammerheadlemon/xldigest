from PyQt5 import QtWidgets

from xldigest.widgets.base_import_wizard_ui import Ui_baseWizard
from xldigest.widgets.add_portfolio_diag import AddPortfolioDialog


class BaseImportWizard(QtWidgets.QWizard, Ui_baseWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.create_portfolio_button.clicked.connect(self._create_portfolio_diag)

    def _create_portfolio_diag(self):
        diag = AddPortfolioDialog()
        if diag.exec_():
            self.new_portfolio_name = diag.name_lineEdit.text()
            print(self.new_portfolio_name)
