"""Basicspace_calculator.py

	TPSのBasicspace距離を算出するモジュール
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""

# 事前に必要な外部モジュールをインポートする
from Chord import Chord
from Basicspace import Basicspace
from Pitchclass import Pitchclass

class BasicspaceCalculator:
	"""BasicspaceCalculatorクラス

		TPSのベーシックスペース距離を算出する
				
		Attributes:
			chord_a (Chord): 算出元のコードクラス
			chord_b (Chord): 算出元のコードクラス
			a_bs(Basicspace): chord_aのベーシックスペースクラス
			b_bs(Basicspace): chord_bのベーシックスペースクラス
			delta(Int): ベーシックスペース距離

	"""
	def __init__(self):
		self.chord_a = None
		self.chord_b = None
		self.a_bs = None
		self.b_bs = None
		self.delta = None

	def calc_basicspace(self, chord_a, chord_b):
		"""ベーシックスペース距離を算出する

			与えられた2つのコードクラスから、ベーシックスペースを生成して距離を算出する

			Args:
			chord_a (Chord): 算出元のコードクラス
			chord_b (Chord): 算出元のコードクラス
			
			Returns:
				delta (Int): ベーシックスペース距離

		"""
		# 引数をプロパティに記録する
		self.chord_a = chord_a
		self.chord_b = chord_b

		# ベーシックスペースの生成
		self.a_bs = Basicspace(chord_a.get_chordname(), chord_a.get_root(), chord_a.get_minorflag())
		self.b_bs = Basicspace(chord_b.get_chordname(), chord_b.get_root(), chord_b.get_minorflag())

		# 距離の算出
		self.delta = self.delta_basicspace()

		return self.delta

	def delta_basicspace(self):
		"""ベーシックスペース距離を算出する

			プロパティとして保存されているベーシックスペースから、ベーシックスペース距離を算出する
			
			Returns:
				delta (Int): ベーシックスペース距離

		"""
		delta_pos = 0
		delta_neg = 0

		for i in range(12):
			sub = self.a_bs.get_bs()[i] - self.b_bs.get_bs()[i]

			if sub < 0:
				delta_neg += (-1 * sub)
			else:
				delta_pos += sub

		return delta_neg if delta_pos < delta_neg else delta_pos

	def get_last_delta(self):
		"""ベーシックスペース距離のゲッタ（アクセサ）

			最後に算出したベーシックスペース距離を返す
			
			Returns:
				delta (Int): ベーシックスペース距離

		"""
		return self.delta

	def __str__(self):
		"""クラスの文字列化処理
		
			ベーシックスペース距離の算出過程を文字列表示する

		"""
		print(f"Basicspace( {self.chord_a.get_chord_name()} , {self.chord_b.get_chord_name()} ) = {self.delta}")
		print("\tfedcba\t   |   \tfedcba\n---------------\t---+---\t-------")
		for i in range(12):
			buf = Pitchclass(i)
			print(f"{buf.get_name()}\t", end="")
			for j in range(self.a_bs.get_bs()[i]):
				print("*", end="")
			print("\t   |   \t", end="")
			for j in range(self.b_bs.get_bs()[i]):
				print("*", end="")
			print()
