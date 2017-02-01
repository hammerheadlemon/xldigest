import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTableView, QWidget,
                             QTableWidget, QHBoxLayout)

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


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
        self.model.setHeaderData(0, Qt.Horizontal, "Cell_Key")
        self.model.setHeaderData(1, Qt.Horizontal, "Sheet")
        self.model.setHeaderData(2, Qt.Horizontal, "Cell_Reference")

        db_table = QTableView()
        db_table.setModel(self.model)
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
