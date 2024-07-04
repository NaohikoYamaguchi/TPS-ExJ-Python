"""Pitchclass.py

	ピッチクラス（音楽を構成する音を表現するクラス）
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""


class Pitchclass:
	"""Pitchclass:クラス

		mod演算（剰余）演算付き整数(Modint)を利用して音を表現する
				
		Attributes:
			value (modint): 値 数字又は音名で指定
	"""
	def __init__(self, val):
		# 初期化
		self.value = None
		# 値の設定
		if isinstance(val, (int, str)):
			self.set(val)
		else:
			raise TypeError("Invalid type for val. Must be int or str.")

	def get(self):
		"""value（ピッチクラス番号）のゲッタ（アクセサ）

			ピッチクラス番号（0～11）を返す

			Returns:
				value (Int): 値（0～11）
		"""
		return self.value

	def get_name(self):
		"""value（ピッチクラス番号）から生成した英語音名を返す

			ピッチクラス番号から相当する英語音名を生成して返す。
			
			Examples:
				"C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"
			
			Returns:
				name (Str): 英語音名
		"""
		names = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
		return names[self.value] if self.value in range(12) else None

	def get_name_short(self):
		"""value（ピッチクラス番号）から生成した短縮版の英語音名を返す

			ピッチクラス番号から相当する短縮版の英語音名を生成して返す。
			
			Examples:
				"C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"
			
			Returns:
				name (Str): 英語音名
		"""
		# 英語音名を返す（短縮版）
		names_short = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
		return names_short[self.value] if self.value in range(12) else None

	def set(self, val):
		"""value（ピッチクラス番号）のセッタ（アクセサ）

			ピッチクラス番号（0～11）または英語音名を使用してvalueをセットする

		"""
		# ピッチクラスの値を設定
		if isinstance(val, int):
			if 0 <= val <= 11:
				self.value = val
			else:
				raise ValueError("Integer value must be between 0 and 11.")
		elif isinstance(val, str):
			val = val.upper()
			names_to_values = {
				"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
				"E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8, "AB": 8,
				"A": 9, "A#": 10, "BB": 10, "B": 11
			}
			if val in names_to_values:
				self.value = names_to_values[val]
			else:
				raise ValueError("Invalid string value for pitch class.")
		else:
			raise TypeError("Invalid type for val. Must be int or str.")

	def __str__(self):
		"""クラスの文字列化処理
		
			文字列表示する

		"""
		return f"{self.value}({self.get_name()})"


#if __name__ == "__main__":

#	# 使用例
#	pc = PitchClass("D#")
#	print(pc)
#	print(pc.get_name_short())
