# test_video.py
# Test video playback using PySide6's multimedia capabilities to convert a video file into a format that can be displayed in the application. This is a test to ensure that the video playback functionality works correctly within the PySide6 framework.


import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl


app = QApplication(sys.argv)

video = QVideoWidget()
video.resize(800, 500)
video.show()

player = QMediaPlayer()
audio = QAudioOutput()

player.setAudioOutput(audio)
player.setVideoOutput(video)

player.setSource(
    QUrl.fromLocalFile(
        r"D:\Dasig\PPTI\My_APP\PX4_INJECTION_v3\UAV_GCS\assets\videos\splash_bg_fixed.mp4"
    )
)

player.play()

sys.exit(app.exec())