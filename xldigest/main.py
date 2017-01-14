import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget,
                             QDialog, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QToolBar, QVBoxLayout, QWidget)

from widgets import DatamapWindow


class MainWindow(QMainWindow):
    """Create the main window that stores all of the widgets necessary
    for the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super(MainWindow, self).__init__(parent)
        self.resize(1024, 768)
        self.setWindowTitle('xldigest')

        self.widget = QWidget()
        self.layout = QHBoxLayout(self.widget)

        self.menu_bar = self.menuBar()
        self.about_dialog = AboutDialog()
        self.dm_window = DatamapWindow()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)

        self.file_menu()
        self.help_menu()
        self.datamap_menu()

        self.tool_bar_items()

    def datamap_menu(self):
        """Create a Datamap submenu with an Configure Datamap item that opens
        another window."""
        self.datamap_sub_menu = self.menu_bar.addMenu('Datamap')

        self.dm_launch_action = QAction('Configure Datamap', self)
        self.dm_launch_action.setStatusTip(
            'Launch new window to configure datamaps')
        self.dm_launch_action.setShortcut('CTRL+D')
        self.dm_launch_action.triggered.connect(self.dm_launch_widget)

        self.datamap_sub_menu.addAction(self.dm_launch_action)

    def file_menu(self):
        """Create a file submenu with an Open File item that opens
        a file dialog."""
        self.file_sub_menu = self.menu_bar.addMenu('File')

        self.open_action = QAction('Open File', self)
        self.open_action.setStatusTip('Open a file into MainWindow.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.exit_action = QAction('Exit Application', self)
        self.exit_action.setStatusTip('Exit the application.')
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(lambda: QApplication.quit())

        self.file_sub_menu.addAction(self.open_action)
        self.file_sub_menu.addAction(self.exit_action)

    def help_menu(self):
        """Create a help submenu with an About item tha opens an
         about dialog."""
        self.help_sub_menu = self.menu_bar.addMenu('Help')

        self.about_action = QAction('About', self)
        self.about_action.setStatusTip('About the application.')
        self.about_action.setShortcut('CTRL+H')
        self.about_action.triggered.connect(lambda: self.about_dialog.exec_())

        self.help_sub_menu.addAction(self.about_action)

    def tool_bar_items(self):
        """Create a tool bar for the main window."""
        self.tool_bar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
        self.tool_bar.setMovable(False)

    def open_file(self):
        """Open a QFileDialog to allow the user to open a file into
        the application."""
        filename, accepted = QFileDialog.getOpenFileName(self, 'Open File')

        if accepted:
            with open(filename) as file:
                file.read()

    def dm_launch_widget(self):
        """Opens a new window to allow the user to view details about
        the datamaps in use in the application."""
        self.dm_window.show()


class AboutDialog(QDialog):
    """Create the necessary elements to show helpful text in a dialog."""

    def __init__(self, parent=None):
        """Display a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')
        self.resize(300, 200)

        author = QLabel('Matthew Lemon')
        author.setAlignment(Qt.AlignCenter)

        github = QLabel('GitHub: hammerheadlemon')
        github.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(author)
        self.layout.addWidget(github)

        self.setLayout(self.layout)


def main():
    application = QApplication(sys.argv)
    window = MainWindow()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
