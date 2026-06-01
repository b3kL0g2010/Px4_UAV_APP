from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QGraphicsOpacityEffect
)
from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve
)
from PySide6.QtGui import (
    QFont
)
from modules.px4_geotagger.main_window import (
    PX4GeoTaggerWindow
)

from modules.Image_flight_review.main_window import (
    ImageFlightReviewWindow
)

from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtGui import QIcon
from core.utils.resource_path import resource_path

class LauncherWindow(QWidget):

    # ============================================
    # INIT
    # ============================================

    def __init__(self):

        super().__init__()

        self.px4_window = None
        self.image_flight_review_window = None

        self.animations = []

        self.build_ui()

    # ============================================
    # UI
    # ============================================

    def build_ui(self):

        # ----------------------------------------
        # WINDOW
        # ----------------------------------------

        self.setWindowTitle(
            "UAV_GCS Launcher"
        )

        self.setWindowIcon(
            QIcon(

                resource_path(
                    "assets/icons/uav_gcs.ico"
                )
            )
        )

        self.resize(
            1200,
            760
        )

        bg_path = resource_path(
            "assets/images/launcher_bg.jpg"
        )

        bg_path = bg_path.replace(
            "\\",
            "/"
        )

        print(
            "[BACKGROUND]",
            bg_path
        )

        self.setStyleSheet(
            f"""
            QWidget{{
                color: #00F5FF;
                font-family: Consolas;
            }}

            #BackgroundWidget{{
                border-image: url("{bg_path}")
                            0 0 0 0 stretch stretch;
            }}
            """
        )

        # ----------------------------------------
        # ROOT LAYOUT
        # ----------------------------------------

        root_layout = QVBoxLayout(self)

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # ----------------------------------------
        # BACKGROUND
        # ----------------------------------------

        background = QWidget()

        background.setObjectName(
            "BackgroundWidget"
        )

        root_layout.addWidget(
            background
        )

        # ----------------------------------------
        # MAIN LAYOUT
        # ----------------------------------------

        main_layout = QVBoxLayout(
            background
        )

        main_layout.setContentsMargins(
            40,
            30,
            40,
            30
        )

        main_layout.setSpacing(
            25
        )

        # ----------------------------------------
        # TITLE
        # ----------------------------------------

        title = QLabel(
            "UAV_GCS"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            QFont(
                "Consolas",
                34,
                QFont.Bold
            )
        )

        title.setStyleSheet(
            """
            color: #00F5FF;
            border: none;
            """
        )

        subtitle = QLabel(
            "Hybrid UAV Ground Control Platform"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setFont(
            QFont(
                "Consolas",
                14
            )
        )

        subtitle.setStyleSheet(
            """
            color: #9CA3AF;
            border: none;
            """
        )

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            subtitle
        )

        # ----------------------------------------
        # GRID
        # ----------------------------------------

        grid = QGridLayout()

        grid.setSpacing(
            24
        )

        main_layout.addLayout(
            grid
        )

        # ----------------------------------------
        # PX4 CARD
        # ----------------------------------------

        px4_card = self.create_module_card(

            title="PX4 GeoTagger",

            description=(
                "Inject GPS into images "
                "using PX4 ULog telemetry."
            ),

            enabled=True,

            beta=True,

            callback=self.open_px4_geotagger
        )

        grid.addWidget(
            px4_card,
            0,
            0
        )

        # ----------------------------------------
        # REPLAY CARD
        # ----------------------------------------

        image_review__card = self.create_module_card(

            title="Image Flight Review",

            description=(
                "Displays GPS of images into a map "
                "And plot the flight path."
            ),

            enabled=True,

            beta=True,

            callback=self.open_image_flight_review
        )

        grid.addWidget(
            image_review__card,
            0,
            1
        )

        # ----------------------------------------
        # AI CARD
        # ----------------------------------------

        ai_card = self.create_module_card(

            title="AI Inspection",

            description="COMING SOON",

            enabled=False
        )

        grid.addWidget(
            ai_card,
            1,
            0
        )

        # ----------------------------------------
        # SWARM CARD
        # ----------------------------------------

        swarm_card = self.create_module_card(

            title="Swarm Control",

            description="COMING SOON",

            enabled=False
        )

        grid.addWidget(
            swarm_card,
            1,
            1
        )

    # ============================================
    # MODULE CARD
    # ============================================

    def create_module_card(
        self,
        title,
        description,
        enabled=False,
        beta=False,
        callback=None
    ):

        card = QFrame()

        card.setMinimumHeight(
            220
        )

        # ----------------------------------------
        # STYLE
        # ----------------------------------------

        if enabled:

            border = "#00F5FF"

            glow = """
            background-color: rgba(10,20,40,0.95);
            border: 2px solid #00F5FF;
            border-radius: 18px;
            """

        else:

            border = "#1F2937"

            glow = """
            background-color: rgba(15,23,42,0.85);
            border: 2px solid #1F2937;
            border-radius: 18px;
            """

        card.setStyleSheet(
            glow
        )

        # ----------------------------------------
        # LAYOUT
        # ----------------------------------------

        layout = QVBoxLayout()

        layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        layout.setSpacing(
            18
        )

        card.setLayout(
            layout
        )

        # ----------------------------------------
        # TITLE ROW
        # ----------------------------------------

        title_row = QHBoxLayout()

        title_row.setContentsMargins(
            0,
            0,
            0,
            0
        )

        title_row.setSpacing(
            10
        )

        # ----------------------------------------
        # TITLE LABEL
        # ----------------------------------------

        title_label = QLabel(
            title
        )

        title_label.setFont(
            QFont(
                "Consolas",
                20,
                QFont.Bold
            )
        )

        title_label.setStyleSheet(
            f"""
            color: {border};
            border: none;
            """
        )

        title_row.addWidget(
            title_label
        )

        # ----------------------------------------
        # BETA BADGE
        # ----------------------------------------

        if beta:

            beta_label = QLabel(
                "BETA"
            )

            beta_label.setAlignment(
                Qt.AlignCenter
            )

            beta_label.setFixedSize(
                46,
                18
            )

            beta_label.setStyleSheet(
                """
                QLabel{
                    background-color: rgba(255,215,0,0.10);

                    color: #FFD700;

                    border: 1px solid #FFD700;

                    border-radius: 8px;

                    font-size: 8px;

                    font-weight: bold;

                    padding-bottom: 1px;
                }
                """
            )

            # ------------------------------------
            # GLOW EFFECT
            # ------------------------------------

            glow_effect = QGraphicsOpacityEffect()

            beta_label.setGraphicsEffect(
                glow_effect
            )

            # SAVE EFFECT REFERENCE
            self.animations.append(
                glow_effect
            )

            # ------------------------------------
            # PULSE ANIMATION
            # ------------------------------------

            glow_anim = QPropertyAnimation(
                glow_effect,
                b"opacity"
            )

            glow_anim.setDuration(  # Lower Value = Faster Animation, Higher Value = Slower Animation
                900
            )

            glow_anim.setStartValue(
                0.25
            )

            glow_anim.setEndValue(
                1.0
            )

            glow_anim.setLoopCount(
                -1
            )

            glow_anim.setEasingCurve(
                QEasingCurve.InOutSine
            )

            # IMPORTANT:
            # AUTO REVERSE EFFECT

            glow_anim.finished.connect(
                lambda: None
            )

            glow_anim.start()

            # SAVE REFERENCE
            self.animations.append(
                glow_anim
            )

            # ------------------------------------
            # POSITIONING
            # ------------------------------------

            title_row.addWidget(
                beta_label,
                alignment=Qt.AlignTop
            )

        # ----------------------------------------
        # PUSH CONTENT LEFT
        # ----------------------------------------

        title_row.addStretch()

        # ----------------------------------------
        # ADD TITLE ROW
        # ----------------------------------------

        layout.addLayout(
            title_row
        )

        # ----------------------------------------
        # DESCRIPTION
        # ----------------------------------------
        desc_label = QLabel(
            description
        )
        desc_label.setWordWrap(
            True
        )
        desc_label.setFont(
            QFont(
                "Consolas",
                11
            )
        )
        desc_label.setStyleSheet(
            """
            color: #D1D5DB;
            border: none;
            """
        )
        layout.addWidget(
            desc_label
        )
        layout.addStretch()

        # ----------------------------------------
        # BUTTON
        # ----------------------------------------

        button = QPushButton()

        if enabled:

            button.setText(
                "OPEN MODULE"
            )
            if callback:

                button.clicked.connect(
                    callback
                )
            
            button.setStyleSheet(
                """
                QPushButton{
                    background-color: #00F5FF;
                    color: black;
                    border-radius: 12px;
                    padding: 14px;
                    font-size: 14px;
                    font-weight: bold;
                }

                QPushButton:hover{
                    background-color: #67E8F9;
                }
                """
            )

        else:
            button.setText(
                "COMING SOON"
            )
            button.setEnabled(
                False
            )
            button.setStyleSheet(
                """
                QPushButton{
                    background-color: #111827;
                    color: #6B7280;
                    border-radius: 12px;
                    padding: 14px;
                    border: 1px solid #374151;
                }
                """
            )

        layout.addWidget(
            button
        )

        return card
    
    # ============================================
    # OPEN MODULE
    # ============================================

    def open_px4_geotagger(self):

        self.px4_window = PX4GeoTaggerWindow()

        self.px4_window.show()

        self.close()

    def open_image_flight_review(self):

        self.image_flight_review_window = ImageFlightReviewWindow()

        self.image_flight_review_window.show()

        self.close()