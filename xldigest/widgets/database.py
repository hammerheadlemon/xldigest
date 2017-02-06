import sys

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QTableView, QTableWidget, QWidget)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.resize(500, 450)
        self.setWindowTitle("Datamap Viewer")
        self.db_widget = DatabaseTable(self)
        self.setCentralWidget(self.db_widget)


class DatabaseTable(QWidget):

    def __init__(self, parent=None):
        super(DatabaseTable, self).__init__(parent)
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('db.sqlite')
        self.db.open()
        print(self.db.tables())

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("datamap")
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        print(self.model.rowCount())
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "key")
        self.model.setHeaderData(2, Qt.Horizontal, "value")
        self.model.setHeaderData(3, Qt.Horizontal, "bicc_sheet")
        self.model.setHeaderData(4, Qt.Horizontal, "bicc_cellref")
        self.model.setHeaderData(5, Qt.Horizontal, "gmpp_sheet")
        self.model.setHeaderData(6, Qt.Horizontal, "gmpp_cellref")
        self.model.setHeaderData(7, Qt.Horizontal, "bicc_verification_formula")
        self.model.setHeaderData(8, Qt.Horizontal, "project")
        self.model.setHeaderData(9, Qt.Horizontal, "quarter")
        self.model.setHeaderData(10, Qt.Horizontal, "timestamp")

        db_table = QTableView()
        db_table.setModel(self.model)
        db_table.hideColumn(0)  # don't want the index
        db_table.horizontalHeader().setStretchLastSection(True)

        self.layout = QHBoxLayout()
        self.layout.addWidget(db_table)
        self.setLayout(self.layout)

        db_table.show()


def main():
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()


# copied this code into xldigest
