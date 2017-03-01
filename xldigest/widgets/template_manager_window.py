from PyQt5 import QtCore, QtWidgets

from xldigest.widgets.template_manager_ui import Ui_TemplateManager


class TemplateTableItem:
    def __init__(self, file_name, file_path, template_type):
        self.file_name = file_name
        self.file_path = file_path
        self.template_type = template_type
        self.directory = QtCore.QDir(self.file_path)


class TemplateFilesModel(QtCore.QAbstractTableModel):
    def __init__(self, file_list, parent=None):
        super(TemplateFilesModel, self).__init__(parent)
        self.file_list = file_list
        self.templates_directory = QtCore.QDir(
            "/home/lemon/Documents/xldigest/templates")

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.file_list)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.file_list[0])

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.file_list[row][col]
            return value

    def headerData(self, section, orientation, role):
        headers = ["Name", "Filename", "Type"]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return headers[section]
            else:
                return section + 1


class TemplateManagerWindow(QtWidgets.QWidget, Ui_TemplateManager):
    def __init__(self, parent=None):
        super(TemplateManagerWindow, self).__init__(parent)
        self.setupUi(self)
        self.test_template = TemplateTableItem(
            'BICC Template',
            '/home/lemon/Documents/xldigest/source/bicc_template.xlsx',
            'Test Type'
        )
        self.model = TemplateFilesModel([[
            self.test_template.file_name, self.test_template.file_path,
            self.test_template.template_type
        ]])
        self.tableView.setModel(self.model)
