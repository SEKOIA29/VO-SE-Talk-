import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QWidget, QLabel)
from PyQt6.QtCore import Qt
from .text_analyzer import TextAnalyzer
from .vo_se_engine import VoSeEngineWrapper
# 既存のTimelineWidgetをインポート
# from .timeline_widget import TimelineWidget 

class TalkMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VO-SE Talk - 読み上げエディタ")
        self.resize(1100, 600)

        # モジュールの初期化
        self.analyzer = TextAnalyzer()
        self.engine = VoSeEngineWrapper()

        # レイアウト設定
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- 1. テキスト入力エリア ---
        input_layout = QHBoxLayout()
        self.label = QLabel("テキスト入力:")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("ここに喋らせたい文章を入力してEnter...")
        self.text_input.returnPressed.connect(self.generate_talk) # Enterで生成
        
        self.btn_generate = QPushButton("音声生成")
        self.btn_generate.clicked.connect(self.generate_talk)

        input_layout.addWidget(self.label)
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.btn_generate)
        self.main_layout.addLayout(input_layout)

        # --- 2. タイムラインエリア（既存のものを流用） ---
        # 本来はここにTimelineWidgetを配置
        self.timeline_placeholder = QWidget()
        self.timeline_placeholder.setStyleSheet("background-color: #222; border: 1px solid #444;")
        self.timeline_placeholder.setMinimumHeight(400)
        self.main_layout.addWidget(self.timeline_placeholder)

        # --- 3. 下部コントロール ---
        bottom_layout = QHBoxLayout()
        self.btn_play = QPushButton("再生")
        self.btn_export = QPushButton("WAV書き出し")
        self.btn_export.clicked.connect(self.export_audio)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_play)
        bottom_layout.addWidget(self.btn_export)
        self.main_layout.addLayout(bottom_layout)

    def generate_talk(self):
        """テキストを解析してタイムラインに流し込む"""
        text = self.text_input.text()
        if not text:
            return
        
        print(f"解析開始: {text}")
        # TextAnalyzerで音素とピッチを取得
        talk_events = self.analyzer.analyze_text(text)
        
        # TODO: self.timeline.set_notes(talk_events) 
        # 解析された音素をタイムラインにセットし、画面を更新する
        print(f"{len(talk_events)}個の音素を生成しました。")

    def export_audio(self):
        """現在のノートをWAVに書き出す（前述の保存ダイアログ処理を呼ぶ）"""
        # ここにQFileDialogを使った書き出し処理を記述
        pass

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = TalkMainWindow()
    window.show()
    sys.exit(app.exec())
