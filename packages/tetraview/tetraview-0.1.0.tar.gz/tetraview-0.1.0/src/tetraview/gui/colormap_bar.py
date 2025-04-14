from silx.gui.qt import QWidget, QVBoxLayout, QLabel

class ColorMapBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Color Map Bar")
        layout.addWidget(label)
        self.setLayout(layout)
