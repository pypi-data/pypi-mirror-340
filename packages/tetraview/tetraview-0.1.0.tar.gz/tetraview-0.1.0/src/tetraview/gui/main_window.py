from silx.gui.qt import QMainWindow, QWidget, QGridLayout, Qt

# Import your panels
from .colormap_bar import ColorMapBar
from .volume_selector import VolumeSelector
from .volume_info import VolumeInfo
from .volume_display import VolumeDisplay
from .menu_bar import MenuBar  # Make sure you have this file with the MenuBar definition

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TetraView")
        self.initUI()

    def initUI(self):
        # Create and set up the menu bar at the top of the application.
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)

        # Create and set the central widget.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Use a grid layout to arrange panels in 2x2.
        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Instantiate panels.
        self.colormap_bar = ColorMapBar()
        self.volume_selector = VolumeSelector()
        self.volume_info = VolumeInfo()
        self.volume_display = VolumeDisplay()

        # Add the panels into the grid (row, column).
        layout.addWidget(self.colormap_bar,    0, 0)
        layout.addWidget(self.volume_selector, 0, 1)
        layout.addWidget(self.volume_info,     1, 0)
        layout.addWidget(self.volume_display,  1, 1)

        # Optionally, adjust spacing or margins here.
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
