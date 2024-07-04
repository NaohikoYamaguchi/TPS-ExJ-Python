"""Modint.py

	mod（剰余）演算付き整数クラス
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""

class Modint:
	"""Modintクラス

		mod演算（剰余）演算付き整数クラス。
				
		Attributes:
			value (Int): 値
			mod (Int): 法
	"""
	def __init__(self, val, mod):
		self.mod = mod	# 法の設定
		self.set(val)  # 値の設定

	def get(self):
		"""valueのゲッタ（アクセサ）

			最後に求めたvalueを返す

			Returns:
				value (Int): 値

		"""
		return self.value

	def get_mod(self):
		"""modのゲッタ（アクセサ）

			最後に設定した法を返す

			Returns:
				mod (Int): 法

		"""
		return self.mod

	# 値をセットする
	def set(self, val):
		"""valueのセッタ（アクセサ）

			valueに値を設定する（この時modを法とした剰余演算を行う）
			
			Args:
				val (Int): 値

		"""
		self.value = val % self.mod

	def __str__(self):
		"""クラスの文字列化処理
		
			文字列表示する

		"""
		return f"{self.value} mod {self.mod}"

	# 足し算
	def add(self, other):
		"""加算

			valueに値を加算する。
			
			* 加算する値がintの場合はvalueを加算した後にmodを法とした剰余演算を行う。
			* 加算する値がmodintの場合は、加算する値の法を確認する
				* 加算される値・する値で法が一致しないとエラー
				* 加算される値・する値で法が一致したらvalueを加算した後にmodを法とした剰余演算を行う。

		"""
		if isinstance(other, int):
			buf = (self.value + other) % self.mod
		elif isinstance(other, Modint):
			if other.get_mod() == self.get_mod():
				buf = self.value + other.get()
			else:
				raise ValueError("Divisor mismatch")
		else:
			raise TypeError("Unsupported type for addition")

		self.set(buf)

# 使用例
#if __name__ == "__main__":
#	a = Modint(10, 3)
#	print(a)  # 出力: 1 mod 3
#	a.add(2)
#	print(a)  # 出力: 0 mod 3

