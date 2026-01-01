import ctypes
import os

# C言語側の構造体定義と合わせる (重要)
class C_PhonemeEvent(ctypes.Structure):
    _fields_ = [
        ("pitch_start", ctypes.c_float),
        ("pitch_end", ctypes.c_float),
        ("duration", ctypes.c_float),
        ("lyric", ctypes.c_char_p),
        ("formant_shift", ctypes.c_float)
    ]

class TalkEngineWrapper:
    def __init__(self, lib_path):
        self.lib = ctypes.CDLL(lib_path)
        # 関数の引数型を定義
        self.lib.execute_talk_render.argtypes = [
            ctypes.c_char_p,          # output_path
            ctypes.POINTER(C_PhonemeEvent), # イベント配列
            ctypes.c_int              # イベント数
        ]

    def render_sentence(self, phoneme_events, output_path):
        # PythonのクラスをC用の構造体配列に変換
        count = len(phoneme_events)
        c_array = (C_PhonemeEvent * count)()
        
        for i, py_ev in enumerate(phoneme_events):
            c_array[i].pitch_start = py_ev.pitch_start
            c_array[i].pitch_end = py_ev.pitch_end
            c_array[i].duration = py_ev.duration
            c_array[i].lyric = py_ev.lyric.encode('utf-8')
            c_array[i].formant_shift = py_ev.formant_shift

        # C言語エンジンのレンダリング関数を呼び出し
        self.lib.execute_talk_render(output_path.encode('utf-8'), c_array, count)
