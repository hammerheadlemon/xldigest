from PyQt5 import QtCore, QtWidgets

from xldigest.widgets.template_manager_ui import Ui_TemplateManager


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
        self.model = TemplateFilesModel(
            [["Hello", "Goodbye"], ["More", "Less"]])
        self.tableView.setModel(self.model)
