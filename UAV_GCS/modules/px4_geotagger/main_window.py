from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTextEdit,
    QSizePolicy
)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import (
    QFont,
    QIcon
)
from PySide6.QtCore import QUrl
from core.utils.resource_path import resource_path
# ============================================
# IMPORT PANELS
# ============================================
from modules.px4_geotagger.ui.panels.left_sidebar_panel import (
    LeftSidebarPanel
)
from PySide6.QtWidgets import QPushButton
from modules.px4_geotagger.backend.parsers.ulog_parser import ULogParser
from modules.px4_geotagger.backend.maps.map_generator import MapGenerator
from PySide6.QtWebEngineWidgets import QWebEngineView
from modules.px4_geotagger.backend.image_loader import ImageLoader
import os

from pathlib import Path
from modules.px4_geotagger.backend.exif.exif_writer import ExifWriter

from modules.px4_geotagger.backend.exif.exif_reader import ExifReader

from modules.px4_geotagger.backend.sync.none_sync import NoneSync

from modules.px4_geotagger.backend.sync.time_sync import TimeSync

from PySide6.QtWidgets import (
    QStackedWidget
)

from PySide6.QtGui import QMovie


class PX4GeoTaggerWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.build_ui()


    # ========================================
    # UI
    # ========================================

    def build_ui(self):

        # ------------------------------------
        # WINDOW
        # ------------------------------------

        self.setWindowTitle(
            "PX4 GeoTagger"
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
            880
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

        # ====================================
        # ROOT LAYOUT
        # ====================================

        root_layout = QHBoxLayout()

        root_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        root_layout.setSpacing(
            12
        )

        self.setLayout(
            root_layout
        )

        # ====================================
        # LEFT SIDEBAR
        # ====================================

        self.left_sidebar = LeftSidebarPanel()

        self.left_sidebar.ulog_dropped.connect(
            self.load_ulog
        )
        self.left_sidebar.images_dropped.connect(
            self.load_image_folder
        )
        self.left_sidebar.output_folder_dropped.connect(
            self.set_output_folder
        )
        self.left_sidebar.start_btn.clicked.connect(
            self.start_geotagging
        )

        root_layout.addWidget(
            self.left_sidebar
        )

        # ====================================
        # RIGHT SIDE
        # ====================================

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

        root_layout.addWidget(
            right_container
        )

        # ====================================
        # TOP HEADER
        # ====================================

        self.header_frame = QFrame()

        self.header_frame.setMinimumHeight(
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
            "PX4 GEO TAGGER"
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


        # ====================================
        # MAP PANEL
        # ====================================

        from PySide6.QtWebEngineWidgets import QWebEngineView

        self.map_frame = QFrame()

        self.map_frame.setMinimumHeight(
            420
        )

        self.map_frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(10,20,40,0.95);

                border: 1px solid #00F5FF;

                border-radius: 18px;
            }
            """
        )

        map_layout = QVBoxLayout()

        map_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        map_layout.setSpacing(
            10
        )

        self.map_frame.setLayout(
            map_layout
        )

        # ====================================
        # MAP TITLE
        # ====================================

        map_title = QLabel(
            "3D FLIGHT MAP"
        )

        map_title.setFont(
            QFont(
                "Consolas",
                12,
                QFont.Bold
            )
        )

        map_title.setStyleSheet(
            """
            color: #00F5FF;
            border: none;
            """
        )

        map_layout.addWidget(
            map_title
        )

        # ====================================
        # STACKED VIEW
        # ====================================

        self.stacked_view = QStackedWidget()

        #
        # ------------------------------------
        # PAGE 0
        # GIF PAGE
        # ------------------------------------
        #

        self.gif_label = QLabel()

        self.gif_label.setAlignment(
            Qt.AlignCenter
        )

        self.gif_label.setStyleSheet(
            """
            border: none;
            background: transparent;
            """
        )

        self.movie = QMovie(

            resource_path(

                "modules/px4_geotagger/assets/gif/Earth.gif"
            )
        )

        self.gif_label.setMovie(
            self.movie
        )
        self.movie.setScaledSize(
            QSize(
                700,
                400
            )
        )
        self.movie.start()

        #
        # ------------------------------------
        # PAGE 1
        # MAP PAGE
        # ------------------------------------
        #

        self.map_view = QWebEngineView()

        self.map_view.setStyleSheet(
            """
            border-radius: 14px;
            """
        )

        #
        # ------------------------------------
        # ADD PAGES
        # ------------------------------------
        #

        self.stacked_view.addWidget(
            self.gif_label
        )

        self.stacked_view.addWidget(
            self.map_view
        )

        #
        # ------------------------------------
        # SHOW GIF FIRST
        # ------------------------------------
        #

        self.stacked_view.setCurrentIndex(
            0
        )

        map_layout.addWidget(
            self.stacked_view
        )

        # ====================================
        # ADD TO RIGHT PANEL
        # ====================================

        right_layout.addWidget(
            self.map_frame
        )

        # ====================================
        # LOWER AREA
        # ====================================

        lower_layout = QHBoxLayout()

        lower_layout.setSpacing(
            12
        )

        right_layout.addLayout(
            lower_layout
        )

        # ====================================
        # TIMELINE PANEL
        # ====================================

        self.timeline_frame = QFrame()

        self.timeline_frame.setMinimumHeight(
            240
        )

        self.timeline_frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(10,20,40,0.95);

                border: 1px solid #00F5FF;

                border-radius: 18px;
            }
            """
        )

        timeline_layout = QVBoxLayout()

        self.timeline_frame.setLayout(
            timeline_layout
        )

        timeline_title = QLabel(
            "FLIGHT TIMELINE"
        )

        timeline_title.setFont(
            QFont(
                "Consolas",
                12,
                QFont.Bold
            )
        )

        timeline_title.setStyleSheet(
            """
            color: #00F5FF;
            border: none;
            """
        )

        timeline_placeholder = QLabel(
            "TIMELINE / FLIGHT MODES / DURATION"
        )

        timeline_placeholder.setAlignment(
            Qt.AlignCenter
        )

        timeline_placeholder.setStyleSheet(
            """
            color: #6B7280;
            font-size: 14px;
            """
        )

        timeline_layout.addWidget(
            timeline_title
        )

        timeline_layout.addStretch()

        timeline_layout.addWidget(
            timeline_placeholder
        )

        timeline_layout.addStretch()

        lower_layout.addWidget(
            self.timeline_frame,
            1
        )

        # ====================================
        # CONSOLE PANEL
        # ====================================

        self.console_frame = QFrame()

        self.console_frame.setMinimumHeight(
            240
        )

        self.console_frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(10,20,40,0.95);

                border: 1px solid #00F5FF;

                border-radius: 18px;
            }
            """
        )

        console_layout = QVBoxLayout()

        self.console_frame.setLayout(
            console_layout
        )

        console_title = QLabel(
            "SYSTEM CONSOLE"
        )

        console_title.setFont(
            QFont(
                "Consolas",
                12,
                QFont.Bold
            )
        )

        console_title.setStyleSheet(
            """
            color: #00F5FF;
            border: none;
            """
        )

        self.console_output = QTextEdit()

        self.console_output.setReadOnly(
            True
        )

        self.console_output.setStyleSheet(
            """
            QTextEdit{

                background-color: #000814;

                border: none;

                color: #00FF99;

                padding: 12px;

                font-size: 11px;
            }
            """
        )

        self.console_output.append(
            "[SYSTEM] PX4 GeoTagger Initialized..."
        )

        self.console_output.append(
            "[SYSTEM] Awaiting ULog Input..."
        )

        console_layout.addWidget(
            console_title
        )

        console_layout.addWidget(
            self.console_output
        )

        lower_layout.addWidget(
            self.console_frame,
            1
        )

    # Button for Back to return to Option List
    def return_to_launcher(self):

        from app.launcher_window import LauncherWindow

        self.launcher = LauncherWindow()

        self.launcher.show()

        self.close()


    # Code Block for loading ULog and processing it to generate the map and update the UI accordingly
    def load_ulog(self, ulg_path):

        try:
            #
            # -----------------------------------
            # FILE CONFIRMATION
            # -----------------------------------
            #
            filename = os.path.basename(
                ulg_path
            )

            self.log_console(

                f"[ULOG] FILE DROPPED: {filename}"
            )

            #
            # -----------------------------------
            # PARSE ULOG
            # -----------------------------------
            #

            parser = ULogParser()

            self.flight_data = parser.load(
                ulg_path
            )

            self.log_console(
                "[ULOG] PARSER SUCCESS"
            )

            #
            # -----------------------------------
            # MAP GENERATION
            # -----------------------------------
            #

            map_generator = MapGenerator()

            map_generator.generate(

                self.flight_data,

                "flight_map.html"
            )

            self.refresh_map()

            self.log_console(
                "[MAP] FLIGHT PATH GENERATED"
            )

            #
            # -----------------------------------
            # STATUS UPDATE
            # -----------------------------------
            #

            self.update_flight_status()

            self.log_console(
                "[SYSTEM] TELEMETRY READY"
            )

        except Exception as e:

            self.log_console(

                f"[ERROR] {str(e)}"
            )

    # Code Blocks for auto refresh the Map Area when user drop the file
    def refresh_map(self):

        map_path = Path(
            "flight_map.html"
        ).resolve()

        print(
            "[MAP EXISTS]",
            map_path.exists()
        )

        self.map_view.load(

            QUrl.fromLocalFile(
                str(map_path)
            )
        )

        #
        # SWITCH TO MAP PAGE
        #

        self.stacked_view.setCurrentIndex(
            1
        )


    # Status update block to show the total GPS samples and Home Position after loading the ULog file
    def update_flight_status(self):

           self.left_sidebar.flight_info_label.setText(

                f"""
        FLIGHT DATA LOADED

        GPS Samples:
        {self.flight_data.total_gps_samples}

        Home Position:
        {self.flight_data.home_position}

        Vehicle Type:
        Quadcopter

        Flight Duration:
        Approx. 5 Minutes

        ULog Status:
        VALID

        Images Loaded:
        {len(getattr(self, 'image_paths', []))}
        """
            )


    # Handler for Images dropped signal from the left sidebar panel, it uses the ImageLoader class to load all images from the dropped folder and updates the flight info label with the count of loaded images
    def load_image_folder(self, folder_path):

        reader = ExifReader()

        try:
            loader = ImageLoader()

            self.image_paths = loader.load_folder(
                folder_path
            )
            #
            # -----------------------------------
            # CONSOLE
            # -----------------------------------
            #
            self.log_console(

                f"[IMAGES] FOLDER LOADED"
            )

            self.log_console(

                f"[IMAGES] TOTAL: {len(self.image_paths)}"
            )
            #
            # -----------------------------------
            # STATUS REFRESH
            # -----------------------------------
            #

            self.update_flight_status()
        

        except Exception as e:

            self.log_console(

                f"[ERROR] {str(e)}"
            )

        if len(self.image_paths) > 0:

                capture_time = reader.get_capture_time(
                    self.image_paths[0]
                )

                self.log_console(

                    f"[EXIF] {capture_time}"
                )

    def set_output_folder(self, folder_path):

        self.output_folder = folder_path

        self.log_console(

            f"[OUTPUT] {folder_path}"
        )

    
    def log_console(self, message):

        self.console_output.append(
            message
        )

    # For Testing
    def start_geotagging(self):

        writer = ExifWriter()

        #
        # ------------------------------------
        # VALIDATION
        # ------------------------------------
        #

        if not hasattr(self, "flight_data"):

            self.log_console(
                "[ERROR] ULOG NOT LOADED"
            )

            return

        if not hasattr(self, "image_paths"):

            self.log_console(
                "[ERROR] IMAGES NOT LOADED"
            )

            return

        if not hasattr(self, "output_folder"):

            self.log_console(
                "[ERROR] OUTPUT FOLDER NOT SET"
            )

            return

        #
        # ------------------------------------
        # SYNC MODE
        # ------------------------------------
        #

        mode = self.left_sidebar.sync_combo.currentText()

        parameter = self.left_sidebar.sync_input.text()

        print(
            "[SYNC MODE]",
            mode
        )

        print(
            "[SYNC PARAMETER]",
            parameter
        )
        #
        # ------------------------------------
        # TIME BASED
        # ------------------------------------
        #

        if mode == "Time-Based":

            try:

                interval_seconds = float(
                    parameter
                )

            except ValueError:

                self.log_console(
                    "[ERROR] INVALID TIME INTERVAL"
                )

                return

            sync = TimeSync()

        #
        # ------------------------------------
        # NONE SYNC
        # ------------------------------------
        #

        elif mode == "None (Use EXIF DateTime)":

            sync = NoneSync()

        #
        # ------------------------------------
        # DISTANCE BASED
        # ------------------------------------
        #

        elif mode == "Distance-Based":

            self.log_console(
                "[ERROR] DISTANCE MODE NOT IMPLEMENTED"
            )

            return

        else:

            self.log_console(
                "[ERROR] INVALID SYNC MODE"
            )

            return

        #
        # ------------------------------------
        # FLIGHT DURATION CHECK
        # ------------------------------------
        #

        flight_duration_sec = (

            self.flight_data.utc_times[-1]

            -

            self.flight_data.mission_start_utc

        ) / 1_000_000

        required_duration_sec = (

            (len(self.image_paths) - 1)

            *

            interval_seconds
        )

        self.log_console(

            f"[FLIGHT] {flight_duration_sec:.1f} sec"
        )

        self.log_console(

            f"[REQUIRED] {required_duration_sec:.1f} sec"
        )

        if required_duration_sec > flight_duration_sec:

            self.log_console(
                "[ERROR] INTERVAL TOO LARGE"
            )

            self.log_console(
                "[ERROR] NOT ENOUGH FLIGHT DATA"
            )

            return

        #
        # ------------------------------------
        # START
        # ------------------------------------
        #

        self.log_console(
            "[INFO] STARTING GEO TAGGING..."
        )

        self.log_console(
            f"[MODE] {mode}"
        )

        self.log_console(
            f"[INTERVAL] {interval_seconds} sec"
        )

        self.left_sidebar.progress_bar.setValue(
            0
        )

        self.left_sidebar.progress_bar.setFormat(
            "PROCESSING... %p%"
        )

        total = len(
            self.image_paths
        )

        # Debug Time Sync for first image
        reader = ExifReader()
        first_image_utc = reader.get_capture_utc_usec(

                self.image_paths[0]
            )
        self.flight_data.camera_start_offset_usec = (
            first_image_utc
            -
            self.flight_data.mission_start_utc
        )

        print(
                "[MISSION UTC]",
                self.flight_data.mission_start_utc
            )

        print(
                "[FIRST IMAGE UTC]",
                first_image_utc
            )

        print(
                "[OFFSET SEC]",
                (
                    first_image_utc
                    -
                    self.flight_data.mission_start_utc
                ) / 1_000_000
            )
        print(

            "[CAMERA OFFSET]",

            self.flight_data.camera_start_offset_usec
        )
        

        #
        # ------------------------------------
        # PROCESS IMAGES
        # ------------------------------------
        #
        reader = ExifReader()

        for index, image_path in enumerate(

            self.image_paths

        ):

            # GPS SYNC BASE ON MODE AND PARAMETER SET BY USER
            if mode == "Time-Based":

                gps = sync.get_gps_for_image(

                    index,

                    interval_seconds,

                    self.flight_data
                )

            elif mode == "None (Use EXIF DateTime)":

                image_utc = reader.get_capture_utc_usec(

                    image_path
                )

                gps = sync.get_gps_for_image(

                    image_utc,

                    self.flight_data
                )

            else:

                gps = None

            #
            # SAFETY CHECK
            #

            if gps is None:

                self.log_console(

                    f"[ERROR] IMAGE {index+1} EXCEEDS FLIGHT DURATION"
                )
                self.log_console(

                    "[ERROR] GEO TAGGING ABORTED"
                )

                break


            filename = Path(
                image_path
            ).name

            output_path = Path(
                self.output_folder
            ) / filename

            writer.write_gps(

                image_path,

                str(output_path),

                gps["lat"],

                gps["lon"],

                gps["alt"]
            )

            progress = int(

                (
                    (index + 1)

                    /

                    total
                )

                * 100
            )

            self.left_sidebar.progress_bar.setValue(

                progress
            )

            if index % 10 == 0:

                self.log_console(

                    f"[PROCESSING] {index+1}/{total}"
                )

        #
        # ------------------------------------
        # FINISHED
        # ------------------------------------
        #

        self.left_sidebar.progress_bar.setValue(
            100
        )

        self.left_sidebar.progress_bar.setFormat(
            "COMPLETE %p%"
        )

        self.log_console(
            "[SUCCESS] GEO TAGGING COMPLETE"
        )

