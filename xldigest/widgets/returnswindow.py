from PyQt5 import QtWidgets, QtCore

from xldigest.widgets.returns_tab_ui import Ui_ReturnsUI
from xldigest.database.base_queries import (project_names_per_quarter,
                                            single_project_data)

#  All this from https://www.youtube.com/watch?v=VcN94yMOkyU&t=71s


class Node:
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return "Node"

    def projectIndex(self):
        return ""

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tablevel=-1):
        """
        Enables us to view structure of tree in console.
        """
        output = ""
        tablevel += 1
        for i in range(tablevel):
            output += "\t"
        output += self._name + "\n"
        for child in self._children:
            output += child.log(tablevel)
        tablevel -= 1
        return output

    def __repr__(self):
        return self.log()


class QuarterNode(Node):
    def __init__(self, name, parent):
        super(QuarterNode, self).__init__(name, parent)

    def typeInfo(self):
        return "Quarter"


class ProjectNode(Node):
    def __init__(self, name, parent, db_index=None, mod_index=None):
        super(ProjectNode, self).__init__(name, parent)
        self.db_index = db_index

    def typeInfo(self):
        return "Project"

    def projectIndex(self):
        return self.db_index

    def __str__(self):
        return "Project: db_index: {}".format(self.db_index)


class SelectionTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        """
        Input: Node
        """
        super(SelectionTreeModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """
        Input: QModelIndex
        Output: int
        """
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        """
        Input: QModelIndex
        Output: int
        """
        return 2

    def data(self, index, role):
        """
        Input: QModelIndex, int
        Output: QVariant, strings are cast to QString which is a QVariant.
        """
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return node.name()
            elif index.column() == 1:
                return node.projectIndex()
            else:
                return node.typeInfo()

    def headerData(self, section, orientation, role):
        """
        Input: int, QOrientation, int
        Output: QVariant, strings are cast to QString which is a QVariant.
        """
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Portfolio Viewer"
            if section == 1:
                return "Project Index"
            else:
                return "TypeInfo"

    def flags(self, index):
        """
        Input: QModelIndex
        Output: int (flag)
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        """
        Input: QModelIndex
        Output: QModelIndex
        Should return the parent of the node with the given QModelIndex
        """
        node = index.internalPointer()
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        """
        Input: int, int, QModelIndex
        Output: QModelIndex
        Should return a QModelIndex that corresponds to the given row, column,
        and parent node.
        """
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()


class ReturnsWindow(QtWidgets.QWidget, Ui_ReturnsUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.selectionTree.rootNode = Node("Quarters")
        self.selectionTree.childNode0 = QuarterNode(
            "Q1", self.selectionTree.rootNode)
        self.selectionTree.childNode1 = QuarterNode(
            "Q2", self.selectionTree.rootNode)
        self.model = SelectionTreeModel(self.selectionTree.rootNode)

        # gather the data
        self.project_names(2)  # used for the tree widget

        self.selectionTree.setModel(self.model)
        self.selectionTree.clicked.connect(self.get_single_return_data)

    def project_names(self, quarter_id):
        projects = project_names_per_quarter(quarter_id)
        for project in projects:
            pn = ProjectNode(
                project[1],  # name
                self.selectionTree.childNode1,  # parent
                project[0])  # db_index

    def get_single_return_data(self, index):
        """
        Return a list or lists consisting of key/values from a
        single return. This then gets fed to the model to populate the
        tableview.
        """
        print("Signal triggered", index.internalPointer())
        p = index.internalPointer()
        d = single_project_data(2, p.db_index)
        self.model_simple_return = SimpleReturnModel(d)
        self.returnsTable.setModel(self.model_simple_return)


class SimpleReturnModel(QtCore.QAbstractTableModel):
    """
    The model for the right hand table in the returns window which shows
    a simple display of return data for a single project.
    """
    def __init__(self, data_in=[[]], parent=None, *args):
        super(SimpleReturnModel, self).__init__(parent, *args)
        self.data_in = data_in

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.data_in)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.data_in[0])

    def headerData(self, section, orientation, role):
        headers = [
            "Key",
            "Value"
        ]
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return headers[section]
            else:
                return section + 1

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data_in[row][col]
            return value
