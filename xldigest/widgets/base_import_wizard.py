from PyQt5 import QtWidgets

from xldigest.widgets.base_import_wizard_ui import Ui_base_import_wizard
from xldigest.widgets.dialogs import (AddPortfolioDialog, AddProjectDialog,
                                      AddSeriesDialog, AddSeriesItemDialog)


class BaseImportWizard(QtWidgets.QWizard, Ui_base_import_wizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.projects = []
        self.portfolio = None
        self.series = None
        self.series_items = []
        self.create_portfolio_button.clicked.connect(
            self._create_portfolio_diag)
        self.add_project_button.clicked.connect(self._add_project_diag)
        self.create_series_button.clicked.connect(self._create_series_diag)
        self.create_series_item_button.clicked.connect(self._add_series_item_diag)
        self.portfolio_added_label.setEnabled(False)
        self.series_added_label.setEnabled(False)
        self.added_projects_table.setColumnCount(1)
        self.added_projects_table.setHorizontalHeaderItem(
            0, QtWidgets.QTableWidgetItem("Projects Added"))
        self.added_projects_table.horizontalHeader().setStretchLastSection(
            True)
        self.added_series_item_table.setColumnCount(1)
        self.added_series_item_table.setHorizontalHeaderItem(
            0, QtWidgets.QTableWidgetItem("Series Items Added"))
        self.added_series_item_table.horizontalHeader().setStretchLastSection(
            True)

    def _create_portfolio_diag(self):
        diag = AddPortfolioDialog()
        if diag.exec_():
            self.portfolio = diag.name_lineEdit.text()
            self.portfolio_added_label.setEnabled(True)
            self.portfolio_added_label.setText(self.portfolio)
            print(diag.name_lineEdit.text())

    def _add_project_diag(self):
        diag = AddProjectDialog()
        if diag.exec_():
            new_project_name = diag.name_lineEdit.text()
            self.projects.append(new_project_name)
            rows = self.added_projects_table.rowCount()
            self.added_projects_table.insertRow(rows)
            p_add = QtWidgets.QTableWidgetItem(new_project_name)
            self.added_projects_table.setItem(rows, 0, p_add)

    def _create_series_diag(self):
        diag = AddSeriesDialog()
        if diag.exec_():
            self.series = diag.name_lineEdit.text()
            self.series_added_label.setEnabled(True)
            self.series_added_label.setText(self.series)
            print(diag.name_lineEdit.text())

    def _add_series_item_diag(self):
        diag = AddSeriesItemDialog()
        if diag.exec_():
            new_series_item_name = diag.name_lineEdit.text()
            self.projects.append(new_series_item_name)
            rows = self.added_series_item_table.rowCount()
            self.added_series_item_table.insertRow(rows)
            si_add = QtWidgets.QTableWidgetItem(new_series_item_name)
            self.added_series_item_table.setItem(rows, 0, si_add)
