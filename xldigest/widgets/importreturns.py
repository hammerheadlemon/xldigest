from PyQt5 import QtWidgets, QtGui, QtCore

from mako.template import Template
from mako.runtime import Context

from io import StringIO

import xldigest.database.paths

from xldigest.widgets.import_returns_tab_ui import Ui_ImportManager
from xldigest.widgets.base_import_wizard import BaseImportWizard
from xldigest.process.ingestor import Ingestor
from xldigest.process.template import BICCTemplate
from xldigest.database.base_queries import (
    project_names_in_portfolio, portfolio_names, series_names, series_items,
    get_project_id)


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
        self.comboPortfolio.insertItem(0, "Choose a Portfolio")
        self.comboPortfolio.setCurrentIndex(0)
        self.comboPortfolio.currentIndexChanged.connect(self._portfolio_select)

        self.series_model = self._pop_series_dropdown()
        self.comboSeries.setModel(self.series_model)
        self.comboSeries.insertItem(0, "Choose a Series")
        self.comboSeries.setCurrentIndex(0)
        self.comboSeries.currentIndexChanged.connect(self._series_select)

        self._selected_series_id = 0
        self.series_item_model = self._pop_series_item_dropdown()
        self.comboSeriesItem.setModel(self.series_item_model)
        self.comboSeriesItem.activated.connect(self._series_item_select)

        self.selectedCountLabel.setText("")
        self.base_setup_launch_wizard.clicked.connect(self._launch_wizard_slot)
        self.importButton.clicked.connect(self.import_slot)

    def import_slot(self):
        """Handler to trigger _gather() and _import_files()"""
        print("Gathering....")
        d = self._gather()
        print("Importing...")
        self._import_files(d)

    def _import_files(self, t_data: dict) -> None:
        """
        Import the selected files into the database and associate with the
        correct portfolio and series item. Uses the Ingestor functionality.
        """
        target_files = list(zip(t_data['selected_files'], t_data['selected_project_ids']))
        for filename, p_id in target_files:
            template = BICCTemplate(filename)
            i = Ingestor(
                db_file='/home/lemon/.local/share/xldigest/db.sqlite',
                portfolio_id=t_data['portfolio_id'],
                project_id=p_id,
                series_item_id=t_data['series_item_id'],
                source_file=template
            )
            i.import_single_return()

    def _gather(self) -> dict:
        """
        Gather data from the returns file table and the dropdowns.
        """
        collected_data = {}
        model = self.model_selected_returns
        selected_project_names = []
        selected_project_ids = []
        i = 0
        for p in range(model.rowCount()):
            selected_f_idx = self.model_selected_returns.index(i, 0)
            selected_p_idx = self.model_selected_returns.index(i, 2)
            selected_series_item_id = self.selected_series_item
            selected_portfolio_id = self.selected_portfolio
            project_file_name = model.data(selected_f_idx, QtCore.Qt.DisplayRole)
            project_name = model.data(selected_p_idx, QtCore.Qt.DisplayRole)
            selected_project_names.append(project_name)
            selected_project_ids.append(get_project_id(project_name))
            i += 1
        collected_data['portfolio_id'] = selected_portfolio_id
        collected_data['series_item_id'] = selected_series_item_id
        collected_data['project_file_name'] = project_file_name
        collected_data['project_id'] = get_project_id(project_name)
        collected_data['selected_files'] = self.selected_files
        collected_data['selected_project_names'] = selected_project_names
        collected_data['selected_project_ids'] = selected_project_ids
        collected_data['project_name_id_pairs'] = tuple(zip(
            selected_project_ids, selected_project_names))
        return collected_data

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
        template = Template(verification_template)
        buf = StringIO()
        ctx = Context(buf, data=data)
        template.render_context(ctx)
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
        try:
            self.selectedCountLabel.setText(
                "{} files selected".format(len(self.selected_files)))
        except AttributeError:
            print("No files selected")

    def _portfolio_select(self, index):
        try:
            self.selected_portfolio = self.comboPortfolio.model().item(
                index, 1).data(QtCore.Qt.UserRole)
            print("Selected Portfolio at Index: {} with data {}".format(
                index, self.selected_portfolio))
        except AttributeError:
            print("This selection has no data, but")
            # call a quit function here as we don't want to proceed
            pass

    def _series_select(self, index):
        try:
            self._selected_series_id = self.comboSeries.model().item(
                index, 1).data(QtCore.Qt.UserRole)
            print("Selected Series at Index: {} with data {}".format(
                index, self._selected_series_id))
            # now we call this to populate the series_item dropdown
            self._pop_series_item_dropdown()
            self.comboSeriesItem.setModel(self.series_item_model)
        except AttributeError:
            print("Series selections has no data, but")
            # call a quit function here as we don't want to proceed
            pass
#        self.series_item_model = self._pop_series_item_dropdown()
#        self.comboSeriesItem.setModel(self.series_item_model)

    def _series_item_select(self, index):
        try:
            self.selected_series_item = self.comboSeriesItem.model().item(
                index, 1).data(QtCore.Qt.UserRole)
            print("Selected SeriesItem at Index: {} with data {}".format(
                index, self.selected_series_item))
        except AttributeError:
            print("This selection has no data, but")
            # call a quit function here as we don't want to proceed
            pass

    def _pop_portfolio_dropdown(self):
        self.portfolio_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = portfolio_names()

        for id, name in items:
            item_text = QtGui.QStandardItem(name)
            port_id = QtGui.QStandardItem()
            port_id.setData(id, QtCore.Qt.UserRole)
            self.portfolio_model.appendRow([item_text, port_id])
        return self.portfolio_model

    def _pop_series_dropdown(self):
        self.series_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = series_names()

        for id, name in items:
            item_text = QtGui.QStandardItem(name)
            s_id = QtGui.QStandardItem()
            s_id.setData(id, QtCore.Qt.UserRole)
            self.series_model.appendRow([item_text, s_id])
        return self.series_model

    def _pop_series_item_dropdown(self):
        self.series_item_model = QtGui.QStandardItemModel()

        # this lot will come from the database
        items = series_items(self._selected_series_id)

        for id, name in items:
            item_text = QtGui.QStandardItem(name)
            si_id = QtGui.QStandardItem()
            si_id.setData(id, QtCore.Qt.UserRole)
            self.series_item_model.appendRow([item_text, si_id])
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
