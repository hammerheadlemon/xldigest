from PyQt5 import QtWidgets

from xldigest.database.setup import USER_DATA_DIR, set_up_session


class AddPortfolioDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Portfolio Name")
        self.name_lineEdit = QtWidgets.QLineEdit("Portfolio Name")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                               QtWidgets.QDialogButtonBox.Cancel)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_lineEdit, 0, 1)
        grid.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(grid)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class AddProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Project Name")
        self.name_lineEdit = QtWidgets.QLineEdit("Project Name")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                               QtWidgets.QDialogButtonBox.Cancel)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_lineEdit, 1, 1)
        grid.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(grid)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class AddSeriesDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Series Name")
        self.name_lineEdit = QtWidgets.QLineEdit("Series Name")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                               QtWidgets.QDialogButtonBox.Cancel)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_lineEdit, 0, 1)
        grid.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(grid)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class AddSeriesItemDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        name_label = QtWidgets.QLabel("Series Item Name")
        self.name_lineEdit = QtWidgets.QLineEdit("Series Item Name")
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok |
                                               QtWidgets.QDialogButtonBox.Cancel)
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
        self.setDirectory(USER_DATA_DIR)
        self.exec_()
