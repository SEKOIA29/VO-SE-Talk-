import os
import sys
import pyopenjtalk
import numpy as np

def get_resource_path(relative_path):
    """実行ファイル化してもパスが通るようにするヘルパー関数"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class TextAnalyzer:
    def __init__(self):
        # 辞書フォルダのパスを設定
        self.dict_path = get_resource_path("dict")
        
    def analyze(self, text):
        """
        テキストを解析して、VO-SEエンジンが使える音素・ピッチデータのリストを返す
        """
        # 1. 音素と抑揚の抽出
        # labelsには詳細な情報、featuresには[音素, タイミング, 抑揚]の簡易データが入る
        try:
            # 日本語テキストを解析
            fullcontext = pyopenjtalk.extract_fullcontext(text)
            # 簡易的な音素・ピッチ情報の取得
            # pythonインターフェースで扱いやすい形式
            phonemes = pyopenjtalk.run_frontend(text)
        except Exception as e:
            print(f"解析エラー: {e}")
            return []

        talk_events = []
        current_time = 0.0

        for p_info in phonemes:
            # p_info[0] は音素名, p_info[1] は開始時間, p_info[2] は終了時間 ...
            # ※pyopenjtalkのバージョンにより戻り値が異なるため、
            # ここではVO-SE Talkに最適な簡易形式を想定
            
            p_name = p_info[0]
            if p_name == 'sil' or p_name == 'pau':
                p_name = 'pau' # 無音系はpauに統一
            
            # 音の長さの計算
            duration = 0.12 # デフォルト
            
            # アクセント（抑揚）の計算
            # 62(D4)を高い音、60(C4)を低い音として初期設定
            # 本来はOpenJTalkのアクセント句情報から数値を算出
            pitch = 60
            
            event = {
                "lyric": p_name,
                "start_time": current_time,
                "duration": duration,
                "pitch_start": pitch,
                "pitch_end": pitch   # 2025年版: 開始と終了でピッチを分ける
            }
            
            talk_events.append(event)
            current_time += duration

        return talk_events


