from PySide6.QtWidgets import *

from PySide6.QtCore import *

from PySide6.QtGui import *


class LeftSidebarPanel(QWidget):


    def __init__(self):

        super().__init__()

        self.build_ui()


    def build_ui(self):

        layout = QVBoxLayout()

        self.setLayout(
            layout
        )

        title = QLabel(
            "IMAGE FLIGHT REVIEW"
        )

        layout.addWidget(
            title
        )

        self.image_drop = self.create_drop_area(

            "DROP IMAGE FOLDER HERE"
        )

        layout.addWidget(
            self.image_drop
        )

        layout.addStretch()
        

    def create_drop_area(self, text):

        frame = QFrame()

        frame.setMinimumHeight(
            100
        )

        layout = QVBoxLayout()

        frame.setLayout(
            layout
        )

        label = QLabel(
            text
        )

        label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            label
        )

        frame.drop_label = label

        return frame
    
   