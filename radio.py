import sys,requests
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QAction, QHBoxLayout, QPushButton, QStyle, QShortcut, QInputDialog
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from qdarkstyle import load_stylesheet_pyqt5

stations = requests.get('https://raw.githubusercontent.com/EdwardChess/ChesterRadio/master/stations.txt').json()

class RadioWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.player =  QMediaPlayer()
        self.player.setVolume(100)

        self.radio = QComboBox(self)
        self.radio.setFont(QFont('Comic Sans MS', 10 , QFont.Bold))
        for k,v in stations.items():
            self.radio.addItem(k, v)
        self.radio.setStyleSheet('combobox-popup: 0; color: #fff;')

        layout = QHBoxLayout(self)
        play_btn = QPushButton(self)
        play_btn.clicked.connect(self.play)
        play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        pause_btn = QPushButton(self)
        pause_btn.clicked.connect(self.pause)
        pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        layout.addWidget(play_btn)
        layout.addWidget(pause_btn)
        layout.addWidget(self.radio)

        QShortcut(QKeySequence(Qt.Key_Q), self, self.close)
        QShortcut(QKeySequence(Qt.Key_S), self, self.play)
        QShortcut(QKeySequence(Qt.Key_P), self, self.pause)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(300,50)
        self.show()

    def play(self):
        self.player.setMedia(QMediaContent(QUrl(self.radio.currentData())))
        self.player.play()

    def pause(self):
        self.player.stop()

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())
    win = RadioWindow()
    sys.exit(app.exec_())
