from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QProgressBar
)
from PySide6.QtCore import (
    Qt,
    QTimer,
    QUrl,
    Signal
)
from PySide6.QtGui import (
    QFont
)
from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput
)
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene
)
from PySide6.QtMultimediaWidgets import (
    QGraphicsVideoItem
)
from core.utils.resource_path import (
    resource_path
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


class SplashScreen(QWidget):

    finished = Signal()

    # -------------------------------------------------
    # INIT
    # -------------------------------------------------

    def __init__(self):

        super().__init__()

        self.progress_value = 0

        self.build_ui()

        self.setAttribute(
        Qt.WA_NativeWindow,
        True
        )

        self.setAttribute(
            Qt.WA_DontCreateNativeAncestors,
            True
        )

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_ui(self):

        # ---------------------------------------------
        # WINDOW
        # ---------------------------------------------

        self.setWindowTitle(
            "UAV_GCS Bootloader"
        )

        self.setWindowIcon(
            QIcon(
                resource_path(
                    "assets/icons/uav_gcs.ico"
                )
            )
        )

        self.resize(
            1280,
            720
        )

        # ---------------------------------------------
        # MAIN LAYOUT
        # ---------------------------------------------

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # ---------------------------------------------
        # VIDEO WIDGET
        # ---------------------------------------------
        # ------------------------------------------------
        # GRAPHICS VIEW
        # ------------------------------------------------

        self.graphics_view = QGraphicsView()

        self.graphics_view.setStyleSheet(
            "border: none; background:black;"
        )

        self.graphics_view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.graphics_view.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        layout.addWidget(
            self.graphics_view
        )

        # ------------------------------------------------
        # SCENE
        # ------------------------------------------------

        self.scene = QGraphicsScene()

        self.graphics_view.setScene(
            self.scene
        )

        # ------------------------------------------------
        # VIDEO ITEM
        # ------------------------------------------------

        self.video_item = QGraphicsVideoItem()

        self.video_item.setSize(
            self.size()
        )

        self.scene.addItem(
            self.video_item
        )
        

        # ---------------------------------------------
        # MEDIA PLAYER
        # ---------------------------------------------

        self.media_player = QMediaPlayer()

        self.audio_output = QAudioOutput()

        self.media_player.setAudioOutput(
            self.audio_output
        )

        # ------------------------------------------------
        # MEDIA PLAYER OUTPUT
        # ------------------------------------------------

        self.media_player.setVideoOutput(
            self.video_item
        )

        

        video_path = resource_path(
            "assets/videos/splash_bg_fixed.mp4"
        )

        self.media_player.setSource(
            QUrl.fromLocalFile(video_path)
        )

        # ---------------------------------------------
        # OVERLAY
        # ---------------------------------------------

        self.overlay = QWidget(
            self
        )

        self.overlay.setGeometry(
            self.rect()
        )

        self.overlay.setStyleSheet(
            """background-color: rgba(0,0,0,60);
            """
        )

        self.overlay.raise_()

        # ---------------------------------------------
        # OVERLAY LAYOUT
        # ---------------------------------------------

        overlay_layout = QVBoxLayout(
            self.overlay,
            alignment=Qt.AlignCenter
        )

        overlay_layout.setContentsMargins(
            80,
            80,
            80,
            80
        )

        overlay_layout.addStretch()

        # ---------------------------------------------
        # TITLE
        # ---------------------------------------------

        title = QLabel(
            "UAV_GCS"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            """
            color: #00F5FF;
            font-size: 42px;
            font-weight: bold;
            """
        )

        overlay_layout.addWidget(
            title
        )

        

        # ---------------------------------------------
        # SUBTITLE
        # ---------------------------------------------

        subtitle = QLabel(
            "Hybrid UAV Ground Control Platform"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet(
            """
            color: #C0C0C0;
            font-size: 18px;
            """
        )

        overlay_layout.addWidget(
            subtitle
        )

        overlay_layout.addSpacing(
            180
        )
        # ---------------------------------------------
        # PROGRESS BAR
        # ---------------------------------------------

        self.progress = QProgressBar()

        self.progress.setFixedWidth(250)

        self.progress.setValue(0)

        self.progress.setTextVisible(
            True
        )

        self.progress.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #00F5FF;
                border-radius: 12px;
                background-color: rgba(0,0,0,120);
                color: white;
                text-align: center;
                height: 20px;
                font-size: 14px;
            }

            QProgressBar::chunk {
                background-color: #11DCE8;
                border-radius: 10px;
            }
            """
        )

        # ---------------------------------------------
        # MOVE PROGRESS BAR
        # ---------------------------------------------
        progress_layout = QHBoxLayout()
        progress_layout.addSpacing(
            50
        )
        

        progress_layout.addWidget(
            self.progress
        )

        

        overlay_layout.addLayout(
            progress_layout
        )

        overlay_layout.addStretch()

        # ---------------------------------------------
        # STATUS LABEL
        # ---------------------------------------------

        self.status_label = QLabel(
            "Initializing PX4 Telemetry..."
        )

        self.status_label.setStyleSheet(
            """
            color: white;
            font-size: 18px;
            """
        )

        # ---------------------------------------------
        # STATUS POSITION CONTROL
        # ---------------------------------------------

        status_layout = QHBoxLayout()

        status_layout.addStretch()

        status_layout.addWidget(
            self.status_label
        )

        # move RIGHT
        status_layout.addSpacing(
            430  
        )

        overlay_layout.addSpacing(
            -100
        )

        overlay_layout.addLayout(
            status_layout
        )
        

        # ---------------------------------------------
        # TIMER
        # ---------------------------------------------

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_progress
        )

        self.timer.start(
            80
        )

        # ---------------------------------------------
        # PLAY VIDEO
        # ---------------------------------------------

        self.media_player.play()
        self.overlay.raise_()

        self.overlay.show()

    # -------------------------------------------------
    # RESIZE
    # -------------------------------------------------

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self.overlay.setGeometry(
            self.rect()
        )

        self.video_item.setSize(
            self.size()
        )

        self.overlay.raise_()

    # -------------------------------------------------
    # UPDATE PROGRESS
    # -------------------------------------------------

    def update_progress(self):

        self.overlay.raise_()

        self.progress_value += 1

        self.progress.setValue(
            self.progress_value
        )

        if self.progress_value < 20:

            self.status_label.setText(
                "Initializing PX4 Telemetry..."
            )

        elif self.progress_value < 40:

            self.status_label.setText(
                "Loading Flight Core..."
            )

        elif self.progress_value < 60:

            self.status_label.setText(
                "Loading AI Navigation..."
            )

        elif self.progress_value < 80:

            self.status_label.setText(
                "Starting UAV Modules..."
            )

        else:

            self.status_label.setText(
                "Launching UAV_GCS..."
            )

        # ---------------------------------------------

        if self.progress_value >= 100:

            self.timer.stop()

            self.finished.emit()

            self.close()

    def showEvent(self, event):

        super().showEvent(event)

        self.overlay.raise_()

        self.overlay.show()