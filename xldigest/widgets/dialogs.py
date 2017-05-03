from PyQt5 import QtWidgets

from xldigest.database.setup import USER_HOME


class AddPortfolioDialog(QtWidgets.QDialog):

    portfolio = None

    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Portfolio Name")
        if not AddPortfolioDialog.portfolio:
            self.name_lineEdit = QtWidgets.QLineEdit()
        else:
            self.name_lineEdit = QtWidgets.QLineEdit(
                AddPortfolioDialog.portfolio)
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_lineEdit, 0, 1)
        grid.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.setLayout(grid)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # signals
        self.name_lineEdit.textEdited.connect(self.updateUi)

    def set_line_edit_value(self):
        AddPortfolioDialog.portfolio = self.name_lineEdit.text()
        print(AddPortfolioDialog.portfolio)
        return AddPortfolioDialog.portfolio

    def updateUi(self):
        enabled = False
        if not self.name_lineEdit.text() == "":
            enabled = True
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Ok).setEnabled(enabled)


class AddProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Project Name")
        self.name_lineEdit = QtWidgets.QLineEdit()
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_lineEdit, 1, 1)
        grid.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.setLayout(grid)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # signals
        self.name_lineEdit.textEdited.connect(self.updateUi)

    def updateUi(self):
        enabled = False
        if not self.name_lineEdit.text() == "":
            enabled = True
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Ok).setEnabled(enabled)


class AddSeriesDialog(QtWidgets.QDialog):

    series = None

    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Series Name")
        if not AddSeriesDialog.series:
            self.name_lineEdit = QtWidgets.QLineEdit()
        else:
            print("In the else: {}".format(AddSeriesDialog.series))
            self.name_lineEdit = QtWidgets.QLineEdit(
                AddSeriesDialog.series)
        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_lineEdit, 0, 1)
        grid.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.setLayout(grid)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # signals
        self.name_lineEdit.textEdited.connect(self.updateUi)

    def set_line_edit_value(self):
        AddSeriesDialog.series = self.name_lineEdit.text()
        return AddSeriesDialog.series

    def updateUi(self):
        enabled = False
        if not self.name_lineEdit.text() == "":
            enabled = True
        self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Ok).setEnabled(enabled)


class AddSeriesItemDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Series Item Name")
        self.name_lineEdit = QtWidgets.QLineEdit()
        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_lineEdit, 1, 1)
        grid.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(grid)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class AddDatamapFromCSVDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.setDirectory(USER_HOME)


class AddGMPPDatamapFromCSVDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.setDirectory(USER_HOME)


class AddTransposedMasterDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.setDirectory(USER_HOME)
