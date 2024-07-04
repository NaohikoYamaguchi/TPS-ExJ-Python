"""Delta_chord_calculator.py

	TPSの和音間距離を算出するモジュール
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""

# 事前に必要な外部モジュールをインポートする
from Chord import Chord
from Basicspace_calculator import BasicspaceCalculator
from Chord_calculator import ChordCalculator
from Region_calculator import RegionCalculator

class Delta_Chord_calculator:
	"""Delta_Chord_calculatorクラス

		TPSの和音間距離を算出する
				
		Attributes:
			basicspace_cal (BasicspaceCalculator): ベーシックスペース距離算出クラス
			region_cal (RegionCalculator): 調間距離算出クラス
			chord_cal(ChordCalculator): コード間距離算出クラス
			chord_a (Chord): 算出元のコードクラス
			chord_b (Chord): 算出元のコードクラス
			delta(Int): 和音間距離

	"""
	def __init__(self):
		self.basicspace_cal = BasicspaceCalculator()
		self.region_cal = RegionCalculator()
		self.chord_cal = ChordCalculator()
		self.chord_a = None
		self.chord_b = None
		self.delta = 0

	def calc_chord_delta(self, chord_1, chord_2):
		"""和音間距離を算出する

			与えられた2つのコードクラスから、和音間距離を算出する

			Args:
				chord_a (Chord): 算出元のコードクラス
				chord_b (Chord): 算出元のコードクラス
			
			Returns:
				delta (Int): コード距離

		"""
		self.chord_a = chord_1
		self.chord_b = chord_2
		result = self.basicspace_cal.calc_basicspace(self.chord_a, self.chord_b)
		result += self.region_cal.calc_region(self.chord_a, self.chord_b)
		result += self.chord_cal.calc_chord(self.chord_a, self.chord_b)
		self.delta = result
		return self.delta

	def get_last_delta_chord(self):
		"""コード間距離のゲッタ（アクセサ）

			最後に求めたコード間距離を返す

			Returns:
				delta (Int): コード距離

		"""
		return self.chord_cal.get_lastdelta()

	def get_last_delta_region(self):
		"""調間距離のゲッタ（アクセサ）

			最後に求めた調間距離を返す

			Returns:
				delta (Int): 調間距離

		"""
		return self.region_cal.get_last_delta()

	def get_last_delta_basicspace(self):
		"""ベーシックスペース距離のゲッタ（アクセサ）

			最後に求めたベーシックスペース距離を返す

			Returns:
				delta (Int): ベーシックスペース距離

		"""
		return self.basicspace_cal.get_last_delta()

	def __str__(self):
		"""クラスの文字列化処理
		
			和音間距離の算出過程を文字列表示する

		"""
		print("***** Result *****")
		print("Region(", self.chord_a.get_chordname(), "/", self.chord_a.get_keyname(), ",", self.chord_b.get_chordname(), "/", self.chord_b.get_keyname(), ")\t=\t", self.region_cal.get_last_delta(), "\n")
		print("Chord(", self.chord_a.get_chordname(), "/", self.chord_a.get_keyname(), ",", self.chord_b.get_chordname(), "/", self.chord_b.get_keyname(), ")\t=\t", self.chord_cal.get_last_delta(), "\n")
		print("Basicspace(", self.chord_a.get_chordname(), "/", self.chord_a.get_keyname(), ",", self.chord_b.get_chordname(), "/", self.chord_b.get_keyname(), ")\t=\t", self.basicspace_cal.get_last_delta(), "\n")
		print("\ndelta(", self.chord_a.get_chordname(), "/", self.chord_a.get_keyname(), ",", self.chord_b.get_chordname(), "/", self.chord_b.get_keyname(), ")\t=\t", self.delta, "\n\n")
		print("*** Details : Region ***")
		print(self.region_cal)
		print("*** Details : Chord ***")
		print(self.chord_cal)
		print("*** Details : Basicspace ***")
		print(self.basicspace_cal)

# chord_a = Chord("G 7")
# chord_a.set_key("C", False)
# chord_b = Chord("C")
# chord_b.set_key("D", True)ｓ
# test = Delta_Chord_calculator()
# print(test.calc_chord_delta(chord_a, chord_b))
# print(test)