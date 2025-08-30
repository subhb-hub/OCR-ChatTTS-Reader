import sys
import threading
import pytesseract
from PIL import Image
import mss
import torch
import torchaudio
import tempfile
import os
import ChatTTS
from playsound import playsound 
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer
from PyQt6.QtGui import QPainter, QPen, QGuiApplication


# --- Init ChatTTS ---

device = "mps" if torch.mps.is_available() else "cpu"
device = "cuda" if torch.cuda.is_available() else device
print(f"Using device : {device}")
chat = ChatTTS.Chat()
chat.load(compile=False)  
rand_spk = chat.sample_random_speaker()
# if you prefer specific speaker
# rand_spk = torch.load("speaker_1.pt")


params_infer_code = ChatTTS.Chat.InferCodeParams(
    spk_emb=rand_spk,
    temperature=0.3,
    top_P=0.7,
    top_K=20,
)
params_refine_text = ChatTTS.Chat.RefineTextParams(
    prompt='[oral_2][laugh_0][break_6]',
)


class SnippingWidget(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.begin = QPoint()
        self.end = QPoint()

        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: rgba(0,0,0,80);")
        self.setCursor(Qt.CursorShape.CrossCursor)

        self.show()

    def paintEvent(self, event):
        if not self.begin.isNull() and not self.end.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.red, 2)
            painter.setPen(pen)
            rect = QRect(self.begin, self.end).normalized()
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.position().toPoint()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.position().toPoint()
        self.update()

    def mouseReleaseEvent(self, event):
        rect = QRect(self.begin, self.end).normalized()
        self.close()
        if rect.width() > 0 and rect.height() > 0:
            self.callback(rect)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR + ChatTTS Reader")

        self.monitoring_rect = None
        self.last_text = ""

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.do_ocr)

        central = QWidget()
        layout = QVBoxLayout(central)

        btn_layout = QHBoxLayout()
        self.btn_select = QPushButton("1. Pick")
        self.btn_select.clicked.connect(self.select_area)
        self.btn_start = QPushButton("2. Start Monitor")
        self.btn_start.setEnabled(False)
        self.btn_start.clicked.connect(self.start_monitor)
        self.btn_stop = QPushButton("3. Stop Monitor")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_monitor)

        btn_layout.addWidget(self.btn_select)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)

        self.label = QLabel("Select a space")
        self.label.setWordWrap(True)

        layout.addLayout(btn_layout)
        layout.addWidget(self.label)
        self.setCentralWidget(central)
        self.resize(400, 200)

    def select_area(self):
        self.hide()
        self.snip = SnippingWidget(self.area_selected)

    def area_selected(self, rect: QRect):
        self.monitoring_rect = rect
        self.label.setText(f"Selected sapce: {rect.x()},{rect.y()} {rect.width()}x{rect.height()}")
        self.btn_start.setEnabled(True)
        self.showNormal()

    def start_monitor(self):
        if self.monitoring_rect:
            self.last_text = ""
            self.timer.start(2000)  # 每 3 秒 OCR 一次
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
            self.btn_select.setEnabled(False)
            self.label.setText("Monitoring...")

    def stop_monitor(self):
        self.timer.stop()
        self.btn_start.setEnabled(True)
        self.btn_select.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.label.setText("Monitor Stopped")

    def speak(self, text):
        """ChatTTS to speak"""
        def run():
            try:
                wavs = chat.infer(
                    [text],
                    params_refine_text=params_refine_text,
                    params_infer_code=params_infer_code,
                )
                wav_tensor = torch.from_numpy(wavs[0]).unsqueeze(0)
                tmp_path = tempfile.mktemp(suffix=".wav")
                torchaudio.save(tmp_path, wav_tensor, 24000)
                playsound(tmp_path)
                os.remove(tmp_path)
            except Exception as e:
                print("TTS Error:", e)

        threading.Thread(target=run, daemon=True).start()

    def do_ocr(self):
        if not self.monitoring_rect:
            return
        rect = self.monitoring_rect
        try:
            with mss.mss() as sct:
                monitor = {"top": rect.y(), "left": rect.x(),
                           "width": rect.width(), "height": rect.height()}
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            text = pytesseract.image_to_string(img, lang="chi_sim+eng").strip()
            if text and text != self.last_text:
                self.last_text = text
                self.label.setText(text)
                print("Find New content:", text)
                self.speak(text)

        except Exception as e:
            self.label.setText(f"Error: {e}")
            print("OCR Error:", e)
            self.stop_monitor()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
