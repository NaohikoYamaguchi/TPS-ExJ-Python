"""Chord.py

	TPSで和音（コード）を表すモジュール
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""

# 事前に必要な外部モジュールをインポートする
from Pitchclass import Pitchclass

class Chord:
	"""Chordクラス

		TPSの和音（コード）を表現する
				
		Attributes:
			chordname (str): コードネーム
			root (int): 調のルート
			is_minor (Boolean): 長調/短調フラグ(True->短調,False->長調)

	"""
	def __init__(self, chordname):
		# コードネームの初期設定
		self.chordname = chordname
		self.root = None
		self.is_minor = None

	def set_chordname(self, chordname):
		"""コードネームのセッタ（アクセサ）

			与えられたコードネームを記録する

			Args:
				chordname (str): コードネーム

		"""
		self.chordname = chordname

	def set_key(self, root, is_minor):
		"""調を設定する。

			* 引数のうちいずれかがNoneならば設定を削除する
			* 引数が2つ指定されていれば、調ルート音と長調・短調を設定する

			Args:
				root (int): 調のルート
				is_minor (Boolean): 長調/短調フラグ(True->短調,False->長調)

		"""
		if root is None or is_minor is None:
			self.root = None
			self.is_minor = None
		else:
			# ルートの設定
			if isinstance(root, str):
				# 文字（音名）による指定
				buf = Pitchclass(root)
				self.root = buf.get()
			elif isinstance(root, int):
				# 数字による指定
				if 0 <= root <= 11:
					self.root = root
				else:
					# 範囲異常
					raise ValueError("Root value out of range")
			else:
				raise TypeError("Invalid type for root")
			
			# 長調/短調フラグの設定
			if isinstance(is_minor, bool):
				self.is_minor = is_minor
			else:
				raise ValueError("Invalid type for is_minor")

	def get_chordname(self):
		"""コードネームのゲッタ（アクセサ）

			コードネームを返す

			Returns:
				chordname (str): コードネーム

		"""
		return self.chordname

	def get_keyname(self):
		"""調を文字列表現する

			調を文字列表現して返す。

			Returns:
				key (str): 調の文字列表現[@ minor / @ major]

		"""
		buf = Pitchclass(self.root)
		keyname = buf.getname()
		if self.is_minor:
			return f"{keyname} minor"
		else:
			return f"{keyname} major"

	def get_minorflag(self):
		"""短長フラグのゲッタ（アクセサ）

			短長フラグを返す

			Returns:
				is_minor (Boolean): 長調/短調フラグ(True->短調,False->長調)

		"""
		return self.is_minor

	def get_root(self):
		"""ルートのゲッタ（アクセサ）

			ルートを返す

			Returns:
				root (int): 調のルート

		"""
		return self.root

	def __str__(self):
		"""クラスの文字列化処理
		
			コードを文字列表示する

		"""
		info = f"[{self.get_chordname()}]"
		if self.root is not None:
			info += f" in {self.get_keyname()}"
		return info

if __name__ == "__main__":
	a = Chord("C maj 7")
	print (a.get_chordname)

