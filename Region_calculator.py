"""Region_calculator.py

	TPSのRegion距離を算出するモジュール
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""
# 事前に必要な外部モジュールをインポートする
from Chord import Chord
from Basicspace import Basicspace
from Pitchclass import Pitchclass
from Modint import Modint

class RegionCalculator:
	"""ChordCalculatorクラス

	TPSの調間距離を算出する
			
	Attributes:
		chord_a (Chord): 算出元のコードクラス
		chord_b (Chord): 算出元のコードクラス
		delta(Int): コード距離

	"""

	def __init__(self):
		self.chord_a = None
		self.chord_b = None
		self.delta = None

	def calc_region(self, chord_a, chord_b):
		"""調間距離を算出する

		与えられた2つのコードクラスから、調間距離を算出する
		
		Args:
			chord_a (Chord): 算出元のコードクラス
			chord_b (Chord): 算出元のコードクラス
		
		Returns:
			delta (Int): 調間距離

		"""

		self.chord_a = chord_a
		self.chord_b = chord_b
		
		
		key_chord_a = Modint(chord_a.get_root(), 12)
		key_chord_b = Modint(chord_b.get_root(), 12)

		if chord_a.get_minorflag():
			key_chord_a.add(3)

		if chord_b.get_minorflag():
			key_chord_b.add(3)

		region_table = [
			[0, 5, 2, 3, 4, 1, 6, 1, 4, 3, 2, 5],
			[5, 0, 5, 2, 3, 4, 1, 6, 1, 4, 3, 2],
			[2, 5, 0, 5, 2, 3, 4, 1, 6, 1, 4, 3],
			[3, 2, 5, 0, 5, 2, 3, 4, 1, 6, 1, 4],
			[4, 3, 2, 5, 0, 5, 2, 3, 4, 1, 6, 1],
			[1, 4, 3, 2, 5, 0, 5, 2, 3, 4, 1, 6],
			[6, 1, 4, 3, 2, 5, 0, 5, 2, 3, 4, 1],
			[1, 6, 1, 4, 3, 2, 5, 0, 5, 2, 3, 4],
			[4, 1, 6, 1, 4, 3, 2, 5, 0, 5, 2, 3],
			[3, 4, 1, 6, 1, 4, 3, 2, 5, 0, 5, 2],
			[2, 3, 4, 1, 6, 1, 4, 3, 2, 5, 0, 5],
			[5, 2, 3, 4, 1, 6, 1, 4, 3, 2, 5, 0]
		]

		self.delta = region_table[key_chord_a.get()][key_chord_b.get()]

		return self.delta

	def get_last_delta(self):
		"""調間距離のゲッタ（アクセサ）

			最後に求めた調間距離を返す

			Returns:
				delta (Int): 調間距離

		"""
		return self.delta

	def __str__(self):
		"""クラスの文字列化処理
		
			文字列表示する

		"""
		return f"Region({self.chord_a.get_key_name()} , {self.chord_b.get_key_name()}) = {self.delta}"


