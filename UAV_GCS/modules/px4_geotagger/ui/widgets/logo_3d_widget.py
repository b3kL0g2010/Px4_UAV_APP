from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from PySide6.QtWebEngineWidgets import (
    QWebEngineView
)

from PySide6.QtCore import (
    QUrl
)

from core.utils.resource_path import (
    resource_path
)


class Logo3DWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.setLayout(layout)

        self.web = QWebEngineView()

        self.web.setStyleSheet(
            """
            border: none;
            background: transparent;
            """
        )

        layout.addWidget(self.web)

        html_path = resource_path(
            "modules/px4_geotagger/assets/html/threejs_drone_viewer.html"
        )

        self.web.load(
            QUrl.fromLocalFile(html_path)
        )