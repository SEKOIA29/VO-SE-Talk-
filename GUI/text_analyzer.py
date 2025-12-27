import pyopenjtalk
import numpy as np

class TextAnalyzer:
    def __init__(self, dict_path=None):
        # dict_pathが指定されていればその辞書を使用
        self.dict_path = dict_path

    def analyze_text(self, text):
        """
        日本語テキストを解析し、音素リストと初期ピッチ情報を返す
        """
        # 1. Open JTalkでフルコンテキストラベルを抽出
        # 音素(p1, p2...)、アクセント結合情報などが含まれる
        labels = pyopenjtalk.extract_fullcontext(text)
        
        # 2. ラベルから音素列とタイミング、アクセント情報をパース
        # pyopenjtalk.run_frontend は [音素, タイミング, 抑揚] の簡易的な情報を返します
        phonemes_and_accents = pyopenjtalk.run_frontend(text)
        
        talk_events = []
        current_time = 0.0
        
        for info in phonemes_and_accents:
            phoneme = info[0]     # 音素 (例: "k", "o")
            # 簡易的なタイミング割り当て（1音素 0.1秒など）
            # 本来はlabelsのタイミング情報を使うとより正確です
            duration = 0.12 
            
            # Open JTalkのアクセント情報をMIDIノート番号(ピッチ)に変換
            # info[1] に含まれるアクセント情報から基本ピッチを設定
            base_pitch = 62 if info[1] > 0 else 60 # 高い音か低い音かの簡易判定
            
            event = {
                "lyric": phoneme,
                "start_time": current_time,
                "duration": duration,
                "pitch": base_pitch
            }
            talk_events.append(event)
            current_time += duration
            
        return talk_events


