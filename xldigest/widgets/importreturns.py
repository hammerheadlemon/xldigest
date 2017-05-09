import os

from PyQt5 import QtWidgets, QtGui, QtCore

from mako.template import Template
from mako.runtime import Context

from io import StringIO

import xldigest.database.paths

from xldigest.widgets.import_returns_tab_ui import Ui_ImportManager
from xldigest.widgets.base_import_wizard import BaseImportWizard
from xldigest.process.ingestor import Ingestor
from xldigest.process.template import BICCTemplate
from xldigest.database.models import Series
from xldigest.database.connection import Connection
from xldigest.database.base_queries import (
    project_names_in_portfolio, portfolio_names, series_names, series_items,
    projects_with_id)

verification_template = """
<h1>Confirmation required</h1>

<p>You are about to create the following entities in the database. Click OK if you are content
     or Cancel to exit the set-up wizard.
 </p>

 <p style="color:red"><strong>Any existing database file will be destroyed and recreated
  if you go ahead.</strong></p>


<h3>Portfolio</h3>

<table>
    <tr>
        <td>${data['portfolio']}</td>
    </tr>
</table>

<h3>Projects</h3>

<table>
    % for p in data['projects']:
        <tr>
            <td>${p}</td>
        </tr>
    % endfor
</table>

<h3>Series</h3>

<table>
    <tr>
        <td>${data['series']}</td>
    </tr>
</table>

<h3>Series Items</h3>

<table>
    % for p in data['series_items']:
        <tr>
            <td>${p}</td>
        </tr>
    % endfor
</table>
"""


class ImportReturns(QtWidgets.QWidget, Ui_ImportManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.launchFileDialog.clicked.connect(self.get_return_source_files_slot)
        self.portfolio_model = self._pop_portfolio_dropdown()
        self.comboPortfolio.setModel(self.portfolio_model)
        self.comboPortfolio.activated.connect(self._portfolio_select)
        self.series_model = self._pop_series_dropdown()
        self.comboSeries.setModel(self.series_model)
        self.comboSeries.activated.connect(self._series_select)
        self._selected_series_id = 0
        self.series_item_model = self._pop_series_item_dropdown()
        self.comboSeriesItem.setModel(self.series_item_model)

        # signals
        self.comboSeriesItem.activated.connect(self._series_item_select)
        self.selectedCountLabel.setText("")
        self.base_setup_launch_wizard.clicked.connect(self._launch_wizard_slot)
        self.importButton.clicked.connect(self._gather)

    def import_files(self, t_data: tuple) -> None:
        """
        Import the selected files into the database and associate with the
        correct portfolio and series item. Uses the Ingestor functionality.
        """
        # TODO fix this function, too tired to deal with PM 8 May...
        # I need to capture the selected project index in the table
        # dropdown. That should then cross reference a project id in the
        # database, then that id should be used in the Ingestor initiator
        # here
        p_mapping = projects_with_id()
        template = BICCTemplate('/home/lemon/Documents/xldigest/source/bicc_template.xlsx')
        for x in t_data:
            i = Ingestor(
                db_file='/home/lemon/.local/share/xldigest/db.sqlite',
                portfolio_id=t_data[0],
                project_id=p_mapping[t_data[1]], # yeah, this is not right
                series_item_id=t_data[3],
                source_file=template
            )

    def _gather(self) -> tuple:
        """
        Gather data from the returns file table and the dropdowns.
        """
        model = self.model_selected_returns
        i = 0
        for p in range(model.rowCount()):
            f_idx = self.model_selected_returns.index(i, 0)
            p_idx = self.model_selected_returns.index(i, 2)
            selected_series_item_id = self.selected_series_item
            selected_portfolio_id = self.selected_portfolio
            project_file_name = model.data(f_idx, QtCore.Qt.DisplayRole)
            project_name = model.data(p_idx, QtCore.Qt.DisplayRole)
            print(
                (
                    selected_portfolio_id,
                    project_file_name,
                    project_name,
                    selected_series_item_id
                ))
            i += 1
        tup = (
            selected_series_item_id + 1,  # to meet db id
            project_file_name,
            project_name,
            selected_series_item_id + 1  # to meet db ide
        )
        self.import_files(tup)
        return tup

    def _launch_wizard_slot(self):
        warning_dialog = QtWidgets.QDialog(parent=self)
        warning_dialog.setWindowTitle("Here be dragons!")
        warning_label = QtWidgets.QLabel("<b>WARNING</b>: Completing this wizard will "
                                         "delete and re-create any application "
                                         "database from scratch, resulting "
                                         "in data loss.<br><br>"
                                         "If you proceed, you can still Cancel"
                                         " the Wizard at any time.")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                               QtWidgets.QDialogButtonBox.Cancel)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(warning_label, 0, 0)
        grid.addWidget(buttonBox, 1, 0, 1, 2)
        warning_dialog.setLayout(grid)
        buttonBox.accepted.connect(warning_dialog.accept)
        buttonBox.rejected.connect(warning_dialog.reject)
        warning_dialog.show()
        if warning_dialog.exec_():
            self.base_wizard = BaseImportWizard()
            if self.base_wizard.exec_():
                self.base_wizard.populate_data()
                data = self.base_wizard.wizard_data
                self.verify_wizard_data(data)

    def _parse_data(self, data):
        """
        Takes a dict and parses it into an HTML table.
        """
        print(data)
        template = Template(verification_template)
        buf = StringIO()
        ctx = Context(buf, data=data)
        template.render_context(ctx)
        print(buf.getvalue())
        return (buf.getvalue())

    def verify_wizard_data(self, data):
        diag = QtWidgets.QDialog(self.base_wizard)
        diag.setWindowTitle("Verify initial set-up")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                               QtWidgets.QDialogButtonBox.Cancel)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(buttonBox, 1, 0, 1, 2)
        diag.setLayout(grid)
        buttonBox.accepted.connect(diag.accept)
        buttonBox.rejected.connect(diag.reject)
        label = QtWidgets.QLabel(self._parse_data(data))
        grid.addWidget(label, 0, 0)
        if diag.exec_():
            print(data)

    def _make_model_data_list(self, *args):
        """
        Tiny helper method.
        """
        return list(args)

    def get_return_source_files_slot(self):
        """
        Triggered when the self.launchFileDialog button is clicked.

        This opens a QFileDialog window and allows the user to select multiple
        files. These are then used to populuate the SelectedFileModel().

        The selectedFilesWidget is populated by SelectedFileModel. One of its
        columns is editable using a custom delegate (DropDownDelegate), used
        to verify which project applies to each file to be imported.
        """
        self.import_returns_dir_dialog = QtWidgets.QFileDialog()
        self.import_returns_dir_dialog.setFileMode(
            QtWidgets.QFileDialog.ExistingFiles)
        self.import_returns_dir_dialog.setDirectory(xldigest.database.paths.USER_HOME)
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
                sfile = sfile.split('/')[-1]
                l.append(
                    self._make_model_data_list(sfile, "bollocks",
                                               "--Confirm Project Title--"))
            self.model_selected_returns = SelectedFilesModel(l)
            self.selectedFilesWidget.setModel(self.model_selected_returns)
            self.selectedFilesWidget.setItemDelegateForColumn(
                2, DropDownDelegate(self.selectedFilesWidget))
            self.selectedFilesWidget.setEditTriggers(
                QtWidgets.QAbstractItemView.CurrentChanged)
            self.selectedFilesWidget.horizontalHeader().setStretchLastSection(
                True)
            print(l)
        try:
            self.selectedCountLabel.setText(
                "{} files selected".format(len(self.selected_files)))
        except AttributeError:
            print("No files selected")

    def _portfolio_select(self, index):
        self.selected_portfolio = index
        print("got that portfolio sig: {}".format(index))

    def _series_select(self, index):
        """
        This is doing the work of populating the series_model, but also
        adjusting the series_item_model depending on what is selected.
        """
        session = Connection.session()
        idx = self.series_model.index(0, index)
        try:
            self._selected_series_id = session.query(Series.id).filter(
                Series.name == self.series_model.data(
                    idx, QtCore.Qt.DisplayRole)).all()[0][0]
        except IndexError:
            self._selected_series_id = index + 1
            print("There are no SeriesItems that related to Series: {}".format(
                self._selected_series_id))
            self.comboSeriesItem.setModel(QtGui.QStandardItemModel())
            self.comboSeriesItem.clear()
        print("got that series sig: {} - index in db: {}".format(
            self.series_model.data(idx, QtCore.Qt.DisplayRole),
            self._selected_series_id))
        self.series_item_model = self._pop_series_item_dropdown()
        self.comboSeriesItem.setModel(self.series_item_model)

    def _series_item_select(self, index):
        self.selected_series_item = index

    def _pop_portfolio_dropdown(self):
        self.portfolio_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = portfolio_names()

        for item in items:
            item_text = QtGui.QStandardItem(item)
            self.portfolio_model.appendRow(item_text)
        return self.portfolio_model

    def _pop_series_dropdown(self):
        self.series_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = series_names()

        for item in items:
            item_text = QtGui.QStandardItem(item)
            self.series_model.appendRow(item_text)
        return self.series_model

    def _pop_series_item_dropdown(self):
        self.series_item_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = series_items(self._selected_series_id)

        for item in items:
            item_text = QtGui.QStandardItem(item)
            self.series_item_model.appendRow(item_text)
        return self.series_item_model


class DropDownDelegate(QtWidgets.QStyledItemDelegate):
    """
    Used to enable selection of project titles from the database, to associate
    them with the return file we want to import.
    """

    def __init__(self, parent):
        super().__init__(parent)

    # Here we create the editor we want to impose upon the cell in the TableView
    # - in this case it is a combo box.
    def createEditor(self, parent, option, index):
        if index.column() == 2:
            combo = QtWidgets.QComboBox(parent)
            li = sorted(
                project_names_in_portfolio(1))  # TODO hard-coded portfolio just now
            combo.addItems(li)
            combo.currentIndexChanged.connect(self.currentIndexChangedSlot)
            return combo

    # what do we do when combo selection is changed. This requests that we commit
    # the data to the model.
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
        headers = ["File Name", "Status", "Project Name"]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return headers[section]
            else:
                return section + 1

    def flags(self, index):
        if (index.column() == 2):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data_in[row][col]
            return value

    # we need this because the model has to accept a change in data from
    # the ComboDelegate. Without overriding this method, we can change the value
    # in the combo, but the value is not retained in the model
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print("setData", index.row(), index.column(), value)
        self.data_in[index.row()][index.column()] = value
