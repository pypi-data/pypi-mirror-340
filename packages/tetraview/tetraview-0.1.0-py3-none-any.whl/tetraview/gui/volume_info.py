from silx.gui.qt import QWidget, QVBoxLayout, QLabel

class VolumeInfo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Volume Info")
        layout.addWidget(label)
        self.setLayout(layout)
