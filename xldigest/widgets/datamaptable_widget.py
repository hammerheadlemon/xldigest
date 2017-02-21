from PyQt5 import QtWidgets
from xldigest.widgets.datamap import DatamapTableModel


class DatamapTable(QtWidgets.QTableView):
    def __init__(self, *args):
        super(DatamapTable, self).__init__(*args)
        table_data = [["Hi", "Hi", "Hi", "Hi", "Hi", "Hi", "Hi"],
                      ["Hi", "Hi", "Hi", "Hi", "Hi", "Hi", "Hi"],
                      ["Hi", "Hi", "Hi", "Hi", "Hi", "Hi", "Hi"]]
        self.tableModel = DatamapTableModel(table_data, self)
        self.setModel(self.tableModel)
        self.setSortingEnabled(True)
