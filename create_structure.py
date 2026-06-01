from pathlib import Path


# =====================================================
# ROOT PROJECT
# =====================================================

PROJECT_NAME = "UAV_GCS"

ROOT = Path(PROJECT_NAME)


# =====================================================
# FOLDER STRUCTURE
# =====================================================

folders = [

    # ---------------------------------------------
    # APP
    # ---------------------------------------------

    "app",

    # ---------------------------------------------
    # CORE
    # ---------------------------------------------

    "core",
    "core/config",
    "core/utils",
    "core/logger",
    "core/theme",

    # ---------------------------------------------
    # ASSETS (GLOBAL)
    # ---------------------------------------------

    "assets",
    "assets/icons",
    "assets/images",
    "assets/gifs",
    "assets/fonts",
    "assets/qss",

    # ---------------------------------------------
    # CPP
    # ---------------------------------------------

    "cpp",
    "cpp/include",
    "cpp/src",
    "cpp/build",

    # ---------------------------------------------
    # MODULES
    # ---------------------------------------------

    "modules",

    # =============================================
    # PX4 GEOTAGGER MODULE
    # =============================================

    "modules/px4_geotagger",

    "modules/px4_geotagger/ui",
    "modules/px4_geotagger/ui/widgets",
    "modules/px4_geotagger/ui/panels",
    "modules/px4_geotagger/ui/dialogs",

    "modules/px4_geotagger/backend",
    "modules/px4_geotagger/backend/parsers",
    "modules/px4_geotagger/backend/sync",
    "modules/px4_geotagger/backend/exif",
    "modules/px4_geotagger/backend/maps",

    "modules/px4_geotagger/assets",
    "modules/px4_geotagger/assets/html",
    "modules/px4_geotagger/assets/templates",

    # ---------------------------------------------
    # MAP ENGINE
    # ---------------------------------------------

    "modules/map_engine",
    "modules/map_engine/leaflet",
    "modules/map_engine/cesium",

    # ---------------------------------------------
    # LOGS
    # ---------------------------------------------

    "logs",

    # ---------------------------------------------
    # TEMP
    # ---------------------------------------------

    "temp",

    # ---------------------------------------------
    # OUTPUT
    # ---------------------------------------------

    "output",

    # ---------------------------------------------
    # TESTS
    # ---------------------------------------------

    "tests"
]


# =====================================================
# FILE STRUCTURE
# =====================================================

files = {

    # =================================================
    # APP
    # =================================================

    "app/__init__.py": "",

    "app/main.py": '''import sys

from PySide6.QtWidgets import QApplication

from app.splash_screen import SplashScreen


def main():

    app = QApplication(sys.argv)

    window = SplashScreen()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()
''',

    "app/splash_screen.py": "",

    "app/launcher_window.py": "",

    # =================================================
    # CORE
    # =================================================

    "core/__init__.py": "",

    "core/utils/__init__.py": "",

    "core/utils/resource_path.py": '''from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def resource_path(relative_path):

    return str(
        BASE_DIR / relative_path
    )
''',

    "core/logger/logger.py": "",

    "core/theme/theme.py": "",

    # =================================================
    # PX4 MODULE
    # =================================================

    "modules/__init__.py": "",

    "modules/px4_geotagger/__init__.py": "",

    "modules/px4_geotagger/main_window.py": "",

    # ---------------- UI ----------------

    "modules/px4_geotagger/ui/__init__.py": "",

    "modules/px4_geotagger/ui/dashboard.py": "",

    "modules/px4_geotagger/ui/widgets/__init__.py": "",

    "modules/px4_geotagger/ui/widgets/map_widget.py": "",

    "modules/px4_geotagger/ui/widgets/console_widget.py": "",

    "modules/px4_geotagger/ui/widgets/status_widget.py": "",

    "modules/px4_geotagger/ui/widgets/timeline_widget.py": "",

    "modules/px4_geotagger/ui/widgets/progress_widget.py": "",

    "modules/px4_geotagger/ui/panels/control_panel.py": "",

    # ---------------- BACKEND ----------------

    "modules/px4_geotagger/backend/__init__.py": "",

    "modules/px4_geotagger/backend/ulog_parser.py": "",

    "modules/px4_geotagger/backend/image_loader.py": "",

    "modules/px4_geotagger/backend/flight_data.py": "",

    "modules/px4_geotagger/backend/sync/time_sync.py": "",

    "modules/px4_geotagger/backend/sync/distance_sync.py": "",

    "modules/px4_geotagger/backend/exif/exif_writer.py": "",

    "modules/px4_geotagger/backend/parsers/gps_parser.py": "",

    "modules/px4_geotagger/backend/maps/map_generator.py": "",

    # =================================================
    # MAP ENGINE
    # =================================================

    "modules/map_engine/__init__.py": "",

    "modules/map_engine/leaflet/leaflet_map.py": "",

    "modules/map_engine/cesium/cesium_map.py": "",

    # =================================================
    # CPP
    # =================================================

    "cpp/CMakeLists.txt": '''cmake_minimum_required(VERSION 3.10)

project(UAV_GCS_CPP)

set(CMAKE_CXX_STANDARD 17)

add_library(
    telemetry_core
    src/telemetry_core.cpp
)
''',

    "cpp/src/telemetry_core.cpp": '''#include <iostream>

void telemetry_init()
{
    std::cout << "Telemetry Core Initialized" << std::endl;
}
''',

    "cpp/include/telemetry_core.h": '''#pragma once

void telemetry_init();
''',

    # =================================================
    # ROOT FILES
    # =================================================

    ".gitignore": '''__pycache__/
*.pyc
*.pyo
*.pyd
*.log
.env
.vscode/
build/
dist/
temp/
output/
*.spec
''',

    "requirements.txt": '''PySide6
PySide6_Addons
folium
pandas
numpy
opencv-python
Pillow
piexif
pyulog
plotly
pyqtgraph
''',

    "README.md": '''# UAV_GCS

Hybrid UAV Ground Control System
'''
}


# =====================================================
# CREATE FOLDERS
# =====================================================

for folder in folders:

    path = ROOT / folder

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"[DIR] {path}")


# =====================================================
# CREATE FILES
# =====================================================

for file_path, content in files.items():

    full_path = ROOT / file_path

    full_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    full_path.write_text(
        content,
        encoding="utf-8"
    )

    print(f"[FILE] {full_path}")


# =====================================================
# DONE
# =====================================================

print("\\nUAV_GCS STRUCTURE CREATED SUCCESSFULLY")