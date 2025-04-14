from silx.gui.qt import QMenuBar, QMenu, QAction, QMessageBox
from tetraview import __version__

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create "File" menu and add the "Open Volume" action.
        file_menu = QMenu("File", self)
        open_volume_action = QAction("Open Volume", self)
        open_volume_action.triggered.connect(self.open_volume)
        file_menu.addAction(open_volume_action)
        self.addMenu(file_menu)
        
        # Create "About" menu and add an action to display version information.
        about_menu = QMenu("About", self)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)
        self.addMenu(about_menu)
    
    def open_volume(self):
        # Placeholder for file open logic.
        # You could integrate a file dialog here.
        print("Open Volume action triggered.")
    
    def show_about(self):
        version = __version__ 
        QMessageBox.about(self, "About", f"TetraView\nVersion: {version}")
