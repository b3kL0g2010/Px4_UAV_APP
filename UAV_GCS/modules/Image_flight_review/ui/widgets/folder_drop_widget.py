from PySide6.QtWidgets import QLabel

from PySide6.QtCore import Qt


class FolderDropWidget(QLabel):


    def __init__(

        self,

        callback=None
    ):

        super().__init__()

        self.callback = callback

        self.setAcceptDrops(
            True
        )

        self.setAlignment(
            Qt.AlignCenter
        )

        self.setText(

            "DROP IMAGE FOLDER HERE"
        )


    def dragEnterEvent(
        self,
        event
    ):

        event.accept()


    def dropEvent(
        self,
        event
    ):

        path = (

            event.mimeData()

            .urls()[0]

            .toLocalFile()
        )

        if self.callback:

            self.callback(
                path
            )