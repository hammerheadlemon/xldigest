from PyQt5 import QtWidgets, QtCore

from xldigest.widgets.returns_tab_ui import Ui_ReturnsUI

#  All this from https://www.youtube.com/watch?v=VcN94yMOkyU&t=71s


class Node:
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if parent is not None:
            parent.addChild(self)

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
        return 1

    def data(self, index, role):
        """
        Input: QModelIndex, int
        Output: QVariant, strings are cast to QString which is a QVariant.
        """
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            return node.name()

    def headerData(self, section, orientation, role):
        """
        Input: int, QOrientation, int
        Output: QVariant, strings are cast to QString which is a QVariant.
        """
        return "Portfolio Viewer"

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
        super(ReturnsWindow, self).__init__(parent)
        self.setupUi(self)
        self.rootNode = Node("Quarters")
        self.childNode0 = Node("Q1", self.rootNode)
        self.childNode1 = Node("Q2", self.rootNode)
        self.childNode2 = Node("Projects", self.childNode1)
        print(self.rootNode)
        model = SelectionTreeModel(self.rootNode)
        self.seletionTree.setModel(model)
