import sys
#pyinstaller --clean --onedir --windowed --icon=assets/app_icon.ico --add-data "assets;assets" --name GeoTaggerPro --version-file version.txt main.py
#pyinstaller --clean --onefile --windowed --icon=assets/app_icon.ico --add-data "assets;assets" --name GeoTaggerPro_Portable --version-file version.txt main.py


# Working here for building the app, but will move to a separate file later
#  Use this -> python -m PyInstaller --clean --onefile --windowed --icon=assets/app_icon.ico --add-data "assets;assets" --add-data "ui/styles;ui/styles" --name BETALOG_Portable --version-file version.txt app/main.py
#python -m app.main to run this file directly without building, but make sure to have the correct working directory (UAV_LOG_Analyzer) and install the required dependencies first (pip install -r requirements.txt)
# python -m PyInstaller --clean --onedir --windowed --icon=assets/icons/uav_gcs.ico --add-data "assets;assets" --add-data "modules/px4_geotagger/assets;modules/px4_geotagger/assets" --add-data "modules/Image_flight_review/assets;modules/Image_flight_review/assets"--name BETALOG_Test app/main.py 
import os
from PySide6.QtWidgets import QApplication

from app.splash_screen import SplashScreen
from app.launcher_window import LauncherWindow


# ============================================
# GLOBAL WINDOW REFERENCE
# ============================================

launcher_window = None



def main():

    global launcher_window

    # DISABLE WEB SECURITY FOR QWEBENGINEVIEW TO ALLOW LOADING LOCAL HTML FILES WITH JS
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        "--disable-web-security "
        "--disable-features=IsolateOrigins "
        "--disable-site-isolation-trials"
        "--ignore-gpu-blocklist "
        "--enable-gpu-rasterization"
    )

    app = QApplication(sys.argv)

    splash = SplashScreen()

    launcher_window = LauncherWindow()

    # ----------------------------------------
    # SHOW LAUNCHER AFTER SPLASH
    # ----------------------------------------

    def show_launcher():

        launcher_window.show()

    splash.finished.connect(
        show_launcher
    )

    splash.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()