from PyQt5 import QtWidgets, QtGui

from xldigest.widgets.base_import_wizard_ui import Ui_base_import_wizard
from xldigest.widgets.dialogs import (AddPortfolioDialog, AddProjectDialog,
                                      AddSeriesDialog, AddSeriesItemDialog,
                                      AddDatamapFromCSVDialog,
                                      AddGMPPDatamapFromCSVDialog,
                                      AddTransposedMasterDialog)


class BaseImportWizard(QtWidgets.QWizard, Ui_base_import_wizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.projects = []
        self.portfolio = None
        self.series = None
        self.series_items = []
        self.wizard_data = {}


        # signals
        # --------

        # buttons
        self.create_portfolio_button.clicked.connect(
            self._create_portfolio_diag)

        self.add_project_button.clicked.connect(self._add_project_diag)
        self.add_project_button.setEnabled(False)

        self.create_series_button.clicked.connect(self._create_series_diag)
        self.create_series_item_button.clicked.connect(
            self._add_series_item_diag)
        self.create_series_item_button.setEnabled(False)

        self.select_datamap_button.clicked.connect(self._add_datamap_csv_diag)
        self.select_gmpp_datamap_button.clicked.connect(self._add_gmpp_datamap_csv_diag)
        self.select_transposed_master_button.clicked.connect(self._add_transposed_master_diag)

        # table cells

        self.imported_datamap_table.cellClicked.connect(self._clicked_cell_dispathcher)

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
        self.setWindowTitle("Set up xldigest application")

        # datamap page table
        self.imported_datamap_table.setItem(0, 0, QtWidgets.QTableWidgetItem(
            "Datamap File:"))
        self.imported_datamap_table.setItem(1, 0, QtWidgets.QTableWidgetItem(
            "GMPP Datamap File:"))
        self.imported_datamap_table.setItem(2, 0, QtWidgets.QTableWidgetItem(
            "Transposed Master File:"))

        clk_to_select = QtWidgets.QTableWidgetItem("--Click to select file--")
        clk_to_select.setForeground(QtGui.QColor(135, 135, 135))

        self.imported_datamap_table.setItem(0, 1, QtWidgets.QTableWidgetItem(
            clk_to_select))
        self.imported_datamap_table.setItem(1, 1, QtWidgets.QTableWidgetItem(
            clk_to_select))
        self.imported_datamap_table.setItem(2, 1, QtWidgets.QTableWidgetItem(
            clk_to_select))

        self.imported_datamap_table.setHorizontalHeaderItem(
            0, QtWidgets.QTableWidgetItem("Description"))
        self.imported_datamap_table.setHorizontalHeaderItem(
            1, QtWidgets.QTableWidgetItem("File Name"))

    def populate_data(self):
        self.wizard_data = {
            'projects': self.projects,
            'portfolio': self.portfolio,
            'series': self.series,
            'series_items': self.series_items,
            'datamap_csv': self.selected_csv_file[0].split('/')[-1],
            'gmpp_datamap_csv': self.selected_gmpp_csv_file[0].split('/')[-1],
            'transposed_master': self.selected_transposed_master_file
        }

    def _clicked_cell_dispathcher(self, row, col):
        if row == 0 and col == 1:
            self._add_datamap_csv_diag()
        if row == 1 and col == 1:
            self._add_gmpp_datamap_csv_diag()
        if row == 2 and col == 1:
            self._add_transposed_master_diag()

    def _create_portfolio_diag(self):
        diag = AddPortfolioDialog()
        if diag.exec_():
            self.portfolio = diag.set_line_edit_value()
            self.portfolio_added_label.setEnabled(True)
            self.portfolio_added_label.setText(self.portfolio)
            self.add_project_button.setEnabled(True)

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
            self.create_series_item_button.setEnabled(True)

    def _add_series_item_diag(self):
        diag = AddSeriesItemDialog()
        if diag.exec_():
            new_series_item_name = diag.name_lineEdit.text()
            self.series_items.append(new_series_item_name)
            rows = self.added_series_item_table.rowCount()
            self.added_series_item_table.insertRow(rows)
            si_add = QtWidgets.QTableWidgetItem(new_series_item_name)
            self.added_series_item_table.setItem(rows, 0, si_add)

    def _add_datamap_csv_diag(self):
        diag = AddDatamapFromCSVDialog(self)
        diag.show()
        if diag.exec_():
            self.selected_csv_file = diag.selectedFiles()
            self.imported_datamap_table.setItem(
                0, 1, QtWidgets.QTableWidgetItem(
                    self.selected_csv_file[0].split('/')[-1]))

    def _add_gmpp_datamap_csv_diag(self):
        diag = AddGMPPDatamapFromCSVDialog(self)
        diag.show()
        if diag.exec_():
            self.selected_gmpp_csv_file = diag.selectedFiles()
            self.imported_datamap_table.setItem(
                1, 1, QtWidgets.QTableWidgetItem(
                    self.selected_gmpp_csv_file[0].split('/')[-1]))

    def _add_transposed_master_diag(self):
        diag = AddTransposedMasterDialog(self)
        diag.show()
        if diag.exec_():
            self.selected_transposed_master_file = diag.selectedFiles()
            self.imported_datamap_table.setItem(
                2, 1, QtWidgets.QTableWidgetItem(
                    self.selected_transposed_master_file[0].split('/')[-1]))
