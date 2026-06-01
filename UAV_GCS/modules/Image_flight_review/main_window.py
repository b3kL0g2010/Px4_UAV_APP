from PySide6.QtWidgets import *

from PySide6.QtGui import *

from PySide6.QtCore import *

from core.utils.resource_path import (
    resource_path
)

from modules.Image_flight_review.backend.image_loader import (
    ImageLoader
)

from modules.Image_flight_review.ui.widgets.folder_drop_widget import (
    FolderDropWidget
)

from modules.Image_flight_review.backend.exif.exif_reader import (
    ExifReader
)
from modules.Image_flight_review.backend.map_generator import (
    MapGenerator
)
from PySide6.QtWebEngineWidgets import (
    QWebEngineView
)
from pathlib import Path

from PySide6.QtCore import QUrl

from PySide6.QtWidgets import (
    QStackedWidget,
    QLabel
)
from PySide6.QtGui import QMovie

class ImageFlightReviewWindow(QWidget):


    # =====================================
    # INIT
    # =====================================

    def __init__(self):

        super().__init__()
        self.build_ui()

        

        


    # =====================================
    # UI
    # =====================================

    def build_ui(self):

        self.setWindowTitle(
            "Image Flight Review"
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
            800
        )
        self.setStyleSheet(
            """
            QWidget{

                background-color: #020617;

                color: white;

                font-family: Consolas;
            }
            """
        )

        main_layout = QHBoxLayout()

        self.setLayout(
            main_layout
        )

        #
        # ---------------------------------
        # LEFT PANEL
        # ---------------------------------
        #

        left_panel = QFrame()

        left_panel.setMinimumWidth(
            200
        )

        left_panel.setStyleSheet(
            """
            QFrame{

                background-color:#0f172a;

                border:1px solid #00F5FF;

                border-radius:14px;
            }
            """
        )

        left_layout = QVBoxLayout()

        left_panel.setLayout(
            left_layout
        )

        #
        # TITLE
        #

        title = QLabel(
            "IMAGE FLIGHT REVIEW"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            QFont(
                "Consolas",
                12,
                QFont.Bold
            )
        )

        title.setStyleSheet(
            """
            color:#00F5FF;
            border:none;
            """
        )

        left_layout.addWidget(
            title
        )

        #
        # DROP AREA
        #

        self.drop_widget = FolderDropWidget(

            callback=self.load_image_folder
        )

        self.drop_widget.setMinimumHeight(
            200
        )
        self.drop_widget.setFixedHeight(
            100
        )

        self.drop_widget.setStyleSheet(
            """
            QLabel{

                border:2px dashed #00F5FF;

                border-radius:12px;

                color:white;

                font-size:14px;

                background-color:#111827;
            }
            """
        )

        left_layout.addWidget(
            self.drop_widget
        )

        #
        # INFO
        #

        self.info_label = QLabel(
            "No Images Loaded"
        )

        self.info_label.setAlignment(
            Qt.AlignCenter
        )

        self.info_label.setStyleSheet(
            """
            color:white;
            border:none;
            """
        )

        left_layout.addWidget(
            self.info_label
        )

        left_layout.addStretch()

        #
        # ADD LEFT PANEL
        #

        main_layout.addWidget(
            left_panel,
            1
        )

        right_container = QWidget()

        right_layout = QVBoxLayout()

        right_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        right_layout.setSpacing(
            12
        )

        right_container.setLayout(
            right_layout
        )

        main_layout.addWidget(
            right_container,
            4
        )

        # ====================================
        # TOP HEADER
        # ====================================

        self.header_frame = QFrame()

        self.header_frame.setMinimumHeight(
            30
        )
        self.header_frame.setFixedHeight(
            70
        )

        self.header_frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(10,20,40,0.95);

                border: 1px solid #00F5FF;

                border-radius: 16px;
            }
            """
        )

        header_layout = QHBoxLayout()

        self.header_frame.setLayout(
            header_layout
        )

        header_title = QLabel(
            "IMAGE FLIGHT REVIEW"
        )

        header_title.setFont(
            QFont(
                "Consolas",
                18,
                QFont.Bold
            )
        )

        header_title.setStyleSheet(
            """
            color: #00F5FF;
            border: none;
            """
        )

        header_layout.addWidget(
            header_title
        )

        # Button to Go Back to Main Menu (Placeholder, no functionality yet)
        self.back_button = QPushButton(
            "← BACK"
        )
        self.back_button.setStyleSheet(
            """
            QPushButton{
                background-color: rgba(0,0,0,120);
                color: #00F5FF;
                border: 1px solid #00F5FF;
                border-radius: 10px;
                padding: 8px 18px;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover{
                background-color: #00F5FF;
                color: black;
            }
            """
        )
        # Push the back button to the right side of the header

        header_layout.addStretch()

        header_layout.addWidget(  # Add the back button to the header layout
            self.back_button
        )

        right_layout.addWidget(
            self.header_frame
        )

        # Connect the back button to a placeholder function
        self.back_button.clicked.connect( 
             self.return_to_launcher
        )

        #
        # STACKED VIEW , GIF + MAP
        #
        self.stacked_view = QStackedWidget()

        #
        # PAGE 0
        # GIF PAGE
        #

        self.gif_label = QLabel()

        self.gif_label.setAlignment(
            Qt.AlignCenter
        )

        self.gif_label.setSizePolicy(

            QSizePolicy.Expanding,

            QSizePolicy.Expanding
        )

        gif_path = resource_path(
            "modules/Image_flight_review/assets/gif/photog.webp"
        )

        self.movie = QMovie(
            gif_path
        )
        self.movie.setScaledSize(
            QSize(1200, 800)
        )

        self.gif_label.setMovie(
            self.movie
        )

        self.movie.start()

        #
        # PAGE 1
        # MAP PAGE
        #

        self.map_view = QWebEngineView()

        #
        # ADD PAGES
        #

        self.stacked_view.addWidget(
            self.gif_label
        )

        self.stacked_view.addWidget(
            self.map_view
        )

        #
        # SHOW GIF FIRST
        #

        self.stacked_view.setCurrentIndex(
            0
        )

        right_layout.addWidget(
            self.stacked_view
        )


    # =====================================
    # IMAGE LOADING
    # =====================================

    def load_image_folder(
        self,
        folder_path
    ):

        loader = ImageLoader()

        reader = ExifReader()

        self.image_paths = (

            loader.load_folder(
                folder_path
            )
        )

        self.image_records = []

        for image_path in self.image_paths:

            gps = reader.get_location(
                image_path
            )

            print(
                "[GPS RESULT]",
                gps
            )

            if gps:

                self.image_records.append({

                    "file":
                        image_path,

                    "lat":
                        gps["lat"],

                    "lon":
                        gps["lon"],

                    "alt":
                        gps["alt"]
                })

        #
        # GENERATE MAP ONCE
        #

        if self.image_records:

            generator = MapGenerator()

            generator.generate(

                self.image_records,

                "image_review_map.html"
            )

            map_path = Path(
                "image_review_map.html"
            ).resolve()

            print(
                "[MAP FILE]",
                map_path
            )

            print(
                "[EXISTS]",
                map_path.exists()
            )

            self.map_view.load(

                QUrl.fromLocalFile(
                    str(map_path)
                )
            )
            self.stacked_view.setCurrentIndex(
                1
            )

            print(
                "[MAP GENERATED]"
            )

        #
        # STATS
        #

        print(

            "[IMAGES FOUND]",

            len(
                self.image_paths
            )
        )

        print(

            "[GPS FOUND]",

            len(
                self.image_records
            )
        )

        gps_count = len(
            self.image_records
        )

        missing_gps = (

            len(self.image_paths)

            -

            gps_count
        )

        if gps_count > 0:

            start = self.image_records[0]

            end = self.image_records[-1]

            altitudes = [

                record["alt"]

                for record in self.image_records
            ]

            min_alt = min(
                altitudes
            )

            max_alt = max(
                altitudes
            )

            self.info_label.setText(

                f"Images: {len(self.image_paths)}\n"

                f"GPS: {gps_count}\n"

                f"Missing: {missing_gps}\n\n"

                f"Start:\n"

                f"{start['lat']:.6f}\n"

                f"{start['lon']:.6f}\n\n"

                f"End:\n"

                f"{end['lat']:.6f}\n"

                f"{end['lon']:.6f}\n\n"

                f"Altitude:\n"

                f"{min_alt:.1f}m - {max_alt:.1f}m"
            )


    def return_to_launcher(self):
        from app.launcher_window import (
            LauncherWindow
        )

        self.launcher = LauncherWindow()

        self.launcher.show()

        self.close()

