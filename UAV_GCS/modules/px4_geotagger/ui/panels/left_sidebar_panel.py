from fileinput import filename

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QFrame,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from modules.px4_geotagger.ui.widgets.logo_3d_widget import (
    Logo3DWidget
)
from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Signal
import  os


class LeftSidebarPanel(QWidget):
    # ====================================
    # INIT
    # ====================================
    ulog_dropped = Signal(str)  # Signal emitted when a ULog file is dropped, carrying the file path as a string
    images_dropped = Signal(str) # Signal emitted when an image folder is dropped, carrying the folder path as a string
    output_folder_dropped = Signal(str) # Signal emitted when an output folder is dropped, carrying the folder path as a strings
    def __init__(self):
        super().__init__()
    
        self.setAcceptDrops(True)
        self.build_ui()
        # =========================================
        # DRAG ENTER
        # =========================================
        def dragEnterEvent(self, event):

            if event.mimeData().hasUrls():

                event.acceptProposedAction()

            else:

                event.ignore()
        # =========================================
        # DROP EVENT
        # =========================================

        def dropEvent(self, event):

            files = event.mimeData().urls()

            if not files:

                return

            file_path = files[0].toLocalFile()

            print(
                "[DROP DETECTED]",
                file_path
            )


            #
            # ----------------------------------------
            # ULOG FILE
            # ----------------------------------------
            #

            if os.path.isfile(file_path):

                if file_path.lower().endswith(".ulg"):

                    print(
                        "[ULOG DROPPED]"
                    )

                    self.ulog_dropped.emit(
                        file_path
                    )

                    event.acceptProposedAction()

                    return
            #
            # ----------------------------------------
            # IMAGE FOLDER
            # ----------------------------------------
            #

            if os.path.isdir(file_path):

                print(
                    "[IMAGE FOLDER DROPPED]"
                )

                self.images_dropped.emit(
                    file_path
                )

                event.acceptProposedAction()

                return
            #
            # ----------------------------------------
            # INVALID
            # ----------------------------------------
            #

            print(
                "[INVALID DROP]"
            )

            event.ignore()

    # ====================================
    # UI
    # ====================================

    def build_ui(self):

        # --------------------------------
        # MAIN STYLE
        # --------------------------------

        self.setStyleSheet(
            """
            QWidget{
                background-color: rgba(5,10,20,0.92);
                color: #E5E7EB;
                font-family: Consolas;
            }
            """
        )

        self.setMinimumWidth(
            340
        )

        self.setMaximumWidth(
            380
        )

        # --------------------------------
        # MAIN LAYOUT
        # --------------------------------

        layout = QVBoxLayout()

        layout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        layout.setSpacing(
            14
        )

        self.setLayout(
            layout
        )

        # =================================
        # 3D LOGO PANEL
        # =================================

        self.logo_frame = QFrame()

        self.logo_frame.setMinimumHeight(
            260
        )

        self.logo_frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(10,20,40,0.95);

                border: 1px solid #00F5FF;

                border-radius: 16px;
            }
            """
        )

        logo_layout = QVBoxLayout()

        logo_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        self.logo_frame.setLayout(
            logo_layout
        )

        # --------------------------------
        # 3D DRONE WIDGET
        # --------------------------------

        self.logo_3d = Logo3DWidget()

        logo_layout.addWidget(
            self.logo_3d
        )

        layout.addWidget(
            self.logo_frame
        )
        
        # =================================
        # ULOG DROP
        # =================================

        self.ulog_drop = self.create_drop_area(
            "DROP PX4 ULOG HERE"
        )

        self.ulog_drop.setAcceptDrops(True)
        self.ulog_drop.dragEnterEvent = self.ulog_drag_enter
        self.ulog_drop.dropEvent = self.ulog_drop_event

        layout.addWidget(
            self.ulog_drop
        )

        # =================================
        # IMAGE DROP
        # =================================

        self.image_drop = self.create_drop_area(
            "DROP IMAGE FOLDER HERE"
        )

        self.image_drop.setAcceptDrops(True)
        self.image_drop.dragEnterEvent = self.image_drag_enter
        self.image_drop.dropEvent = self.image_drop_event

        layout.addWidget(
            self.image_drop
        )

        # =================================
        # OUTPUT DROP
        # =================================

        self.output_drop = self.create_drop_area(
            "DROP OUTPUT FOLDER HERE"
        )

        self.output_drop.setAcceptDrops(True)
        self.output_drop.dragEnterEvent = self.output_drag_enter
        self.output_drop.dropEvent = self.output_drop_event

        layout.addWidget(
            self.output_drop
        )

        # =================================
        # SYNCHRONIZATION
        # =================================

        sync_label = QLabel(
            "Synchronization"
        )

        sync_label.setFont(
            QFont(
                "Consolas",
                11,
                QFont.Bold
            )
        )

        layout.addWidget(
            sync_label
        )

        self.sync_combo = QComboBox()

        self.sync_combo.addItems([

            "Time-Based",
            "Distance-Based",
            "None (Use EXIF DateTime)"

        ])

        self.sync_combo.setStyleSheet(
            self.combo_style()
        )

        layout.addWidget(
            self.sync_combo
        )

        # =================================
        # SYNC PARAMETER INPUT
        # =================================

        self.sync_input = QLineEdit()

        self.sync_input.setPlaceholderText(
            "Interval (seconds)"
        )

        self.sync_input.setStyleSheet(
            self.input_style()
        )

        layout.addWidget(
            self.sync_input
        )

        # =================================
        # COMBO SIGNAL
        # =================================

        self.sync_combo.currentTextChanged.connect(
            self.update_sync_mode
        )

        # =================================
        # START BUTTON
        # =================================

        self.start_btn = QPushButton(
            "START GEO TAGGING"
        )

        self.start_btn.setMinimumHeight(
            52
        )

        self.start_btn.setStyleSheet(
            """
            QPushButton{

                background-color: #00F5FF;

                color: black;

                border-radius: 14px;

                font-size: 14px;

                font-weight: bold;
            }

            QPushButton:hover{

                background-color: #67E8F9;
            }
            """
        )

        layout.addWidget(
            self.start_btn
        )

        # =================================
        # PROGRESS BAR
        # =================================

        self.progress_frame = QFrame()

        self.progress_frame.setMinimumHeight(
            34
        )

        self.progress_frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(15,23,42,0.95);

                border: 1px solid #00F5FF;

                border-radius: 14px;
            }
            """
        )

        progress_layout = QVBoxLayout()

        progress_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        self.progress_frame.setLayout(
            progress_layout
        )

        # --------------------------------
        # PROGRESS BAR
        # --------------------------------

        self.progress_bar = QProgressBar()

        self.progress_bar.setValue(
            0
        )

        self.progress_bar.setFormat(
            "READY  %p%"
        )

        self.progress_bar.setTextVisible(
            True
        )

        self.progress_bar.setMinimumHeight(
            22
        )

        self.progress_bar.setStyleSheet(
            """
            QProgressBar{

                background-color: #000814;

                border: 1px solid #00F5FF;

                border-radius: 10px;

                text-align: center;

                color: white;

                font-weight: bold;
            }

            QProgressBar::chunk{

                background-color: #00F5FF;

                border-radius: 8px;
            }
            """
        )

        progress_layout.addWidget(
            self.progress_bar
        )

        

        layout.addWidget(
            self.progress_frame
        )

        # =================================
        # STATUS
        # =================================

        self.status_frame = QFrame()

        self.status_frame.setMinimumHeight(
            120
        )

        self.status_frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(10,20,40,0.95);

                border: 1px solid #00F5FF;

                border-radius: 16px;
            }
            """
        )

        status_layout = QVBoxLayout()

        self.status_frame.setLayout(
            status_layout

        )
        self.status_frame.setFixedHeight(200
        )

        # =================================
        # STATUS TITLE
        # =================================

        status_title = QLabel(
            "SYSTEM STATUS"
        )

        status_title.setFont(
            QFont(
                "Consolas",
                11,
                QFont.Bold
            )
        )

        status_title.setStyleSheet(
            """
            color: #00F5FF;
            border: none;
            """
        )

        status_layout.addWidget(
            status_title
        )

        # =================================
        # FLIGHT INFO LABEL
        # =================================

        self.flight_info_label = QLabel(

            "NO FLIGHT DATA LOADED"
        )

        self.flight_info_label.setWordWrap(
            True
        )

        self.flight_info_label.setAlignment(
            Qt.AlignTop
        )

        self.flight_info_label.setStyleSheet(
            """
            QLabel {

                color: #00F5FF;

                border: none;

                font-size: 11px;

                padding: 6px;
            }
            """
        )

        status_layout.addWidget(
            self.flight_info_label
        )

        # =================================
        # ADD STATUS FRAME
        # =================================

        layout.addWidget(
            self.status_frame
        )

        layout.addStretch()

        # =================================
        # INITIAL STATE
        # =================================

        self.update_sync_mode()

    # ====================================
    # DROP AREA
    # ====================================

    def create_drop_area(self, text):

        frame = QFrame()
        # Size of the drop area
        frame.setMinimumHeight(
            50
        )

        frame.setStyleSheet(
            """
            QFrame{

                background-color: rgba(10,20,40,0.95);

                border: 2px dashed #374151;

                border-radius: 14px;
            }
            """
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

        label.setStyleSheet(
            """
            color: #00F5FF;
            font-size: 11px;
            font-weight: bold;
            border: none;
            """
        )

        layout.addStretch()

        layout.addWidget(
            label
        )

        layout.addStretch()

        # Save label reference
        frame.drop_label = label

        return frame
                                                
    # ====================================
    # UPDATE SYNC MODE
    # ====================================

    def update_sync_mode(self):

        mode = self.sync_combo.currentText()

        # --------------------------------
        # NONE
        # --------------------------------

        if "None" in mode:

            self.sync_input.setEnabled(
                False
            )

            self.sync_input.setPlaceholderText(
                "EXIF timestamps will be used automatically"
            )

            self.sync_input.clear()

        # --------------------------------
        # TIME
        # --------------------------------

        elif "Time" in mode:

            self.sync_input.setEnabled(
                True
            )

            self.sync_input.setPlaceholderText(
                "Interval (seconds)"
            )

        # --------------------------------
        # DISTANCE
        # --------------------------------

        else:

            self.sync_input.setEnabled(
                True
            )

            self.sync_input.setPlaceholderText(
                "Distance Threshold (meters)"
            )

    # ====================================
    # INPUT STYLE
    # ====================================

    def input_style(self):

        return """
        QLineEdit{

            background-color: rgba(15,23,42,0.95);

            border: 1px solid #374151;

            border-radius: 12px;

            padding: 12px;

            color: white;

            font-size: 11px;
        }
        """

    # ====================================
    # COMBO STYLE
    # ====================================

    def combo_style(self):

        return """
        QComboBox{

            background-color: rgba(15,23,42,0.95);

            border: 1px solid #374151;

            border-radius: 12px;

            padding: 12px;

            color: white;

            font-size: 11px;
        }
        """
    


    # =========================================
    # ULOG DRAG ENTER
    # =========================================

    def ulog_drag_enter(self, event):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

        else:

            event.ignore()


    # =========================================
    # ULOG DROP EVENT
    # =========================================

    def ulog_drop_event(self, event):

        files = event.mimeData().urls()

        if not files:

            return

        file_path = files[0].toLocalFile()

        print(
            "[ULOG DROPPED]",
            file_path
        )
        filename = os.path.basename(file_path)
        self.ulog_drop.drop_label.setText(
            f"✔ {filename}"
        )
        self.ulog_drop.drop_label.setStyleSheet(
            """
            color: #00FF88;
            border: none;
            font-weight: bold;
            """
        )
        self.ulog_drop.setStyleSheet(
                """
                QFrame{

                    background-color: rgba(10,20,40,0.95);

                    border: 2px solid #00FF88;

                    border-radius: 14px;
                }
                """
            )


        if file_path.lower().endswith(".ulg"):

            self.ulog_dropped.emit(
                file_path
            )

            event.acceptProposedAction()

        else:

            event.ignore()


    # =========================================
    # IMAGE DRAG ENTER
    # =========================================

    def image_drag_enter(self, event):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

        else:

            event.ignore()


    # =========================================
    # IMAGE DROP EVENT
    # =========================================

    def image_drop_event(self, event):

        import os

        files = event.mimeData().urls()

        if not files:

            return

        folder_path = files[0].toLocalFile()

        print(
            "[IMAGE FOLDER DROPPED]",
            folder_path
        )
        folder_name = os.path.basename(folder_path)
        self.image_drop.drop_label.setText(
            f"✔ {folder_name}"
        )

        self.image_drop.drop_label.setStyleSheet(
            """
            color: #00FF88;
            border: none;
            font-weight: bold;
            """
        )
        self.image_drop.setStyleSheet(
                """
                QFrame{

                    background-color: rgba(10,20,40,0.95);

                    border: 2px solid #00FF88;

                    border-radius: 14px;
                }
                """
            )

        if os.path.isdir(folder_path):

            self.images_dropped.emit(
                folder_path
            )

            event.acceptProposedAction()

        else:

            event.ignore()



    def output_drag_enter(self, event):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

        else:

            event.ignore()

    def output_drop_event(self, event):

        files = event.mimeData().urls()

        if not files:

            return

        folder_path = files[0].toLocalFile()

        if os.path.isdir(folder_path):

            self.output_folder_dropped.emit(
                folder_path
            )

            folder_name = os.path.basename(
                folder_path
            )

            self.output_drop.drop_label.setText(
                f"✔ {folder_name}"
            )

            self.output_drop.drop_label.setStyleSheet(
                """
                color: #00FF88;
                border: none;
                font-weight: bold;
                """
            )

            self.output_drop.setStyleSheet(
                """
                QFrame{

                    background-color: rgba(10,20,40,0.95);

                    border: 2px solid #00FF88;

                    border-radius: 14px;
                }
                """
            )

            event.acceptProposedAction()

        else:

            event.ignore()