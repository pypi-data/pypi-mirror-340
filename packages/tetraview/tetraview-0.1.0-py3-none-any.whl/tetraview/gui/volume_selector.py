from silx.gui.qt import QWidget, QVBoxLayout, QLabel

class VolumeSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Volume Selector")
        layout.addWidget(label)
        self.setLayout(layout)
