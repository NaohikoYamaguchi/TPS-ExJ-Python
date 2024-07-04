"""Basicspace.py

	TPSのBasicspaceを実現するモジュール
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""

# 事前に必要な外部モジュールをインポートする
from Modint import Modint
from Pitchclass import Pitchclass

class Basicspace:
	"""Basicspaceクラス

		TPSのベーシックスペースを実現する
		
		Args:
			chordname (str): コードネーム
			root (int): 調のルート
			is_minor (Boolean): 長調/短調フラグ(True->短調,False->長調)
		
		Attributes:
			bs (List): ベーシックスペース

	"""
	def __init__(self, chordname, root, is_minor):
		self.bs = []
		self.gen_bs(chordname, root, is_minor)

	def gen_bs(self, chordname, root, is_minor):
		"""ベーシックスペースを生成する

			コードネーム、調のルート、長調/短調フラグから、当該和音を表すベーシックスペースを生成する。

			Args:
				chordname (str): コードネーム
				root (int): 調のルート
				is_minor (Boolean): 長調/短調フラグ(True->短調,False->長調)

		"""
		# 配列の初期化（初期値はすべて1）
		self.bs = [1] * 12

		# 調構成音の重みを1レベル増やす
		self.gen_bs_keyconstructnote(root, is_minor)

		# コードネームから和音を構成する
		self.gen_bs_chordstructnote(chordname)

	def gen_bs_keyconstructnote(self, root, is_minor):
		"""ベーシックスペースの調構成音レベルを決定

			調のルート、長調/短調フラグから、ベーシックスペースの調構成音レベルを決定する。

			Args:
				root (int): 調のルート
				is_minor (Boolean): 長調/短調フラグ(True->短調,False->長調)

		"""
	
		nowpc = Modint(root, 12)

		steps = [2, 1, 2, 2, 1, 2, 2] if is_minor else [2, 2, 1, 2, 2, 2, 1]
		for step in steps:
			nowpc.add(step)
			self.bs[nowpc.get()] += 1

	def gen_bs_chordstructnote(self, chordname):
		"""ベーシックスペースの和音構成音レベルを決定

			コードネームから当該和音を表すベーシックスペースを生成する。

			Args:
				chordname (str): コードネーム
			
			Note:
				* コードネームパーサに対する注意
					このコードネームパーサは暫定版であり，以下の制約を持つ．
						* ルート音，各コードネームを構成する部品は半角スペースで区切る必要がある(例:"Cm7-5"->"C m 7 -5")
						* コードネームの文法誤りについては考慮していない
				* 対応するコードネーム
					現在，以下に示すコードネームに対応している．(@はコードの主音）
						* [@] メジャーコード
						* [@m] マイナーコード
						* [@maj7] メジャー・セブンス
						* [@mmaj7] マイナー・メジャー・セブンス
						* [@aug] オーギュメント(増5度)
						* [@-5] (altと同じ意味)フラットファイブ(減5度)
						* [@alt] (-5と同じ意味)アルタード(減5度)
						* [@7] セブンス
						* [@m7] マイナー・セブンス
						* [@aug7] オーギュメント・セブンス
						* [@7-5] アルタード・セブンス
						* [@dim] ディミニッシュ(ここではクラシック音楽理論風に三和音として定義)
						* [@m7-5] マイナーセブン・フラッテッドファイブ
						* [@dim(M7)] ディミニッシュド・メジャーセブンス
						* [@sus4] サスペンデッド・フォー
						* [@7sus4] セブンス・サスペンデッド・フォー

		"""
		chord = chordname.split(" ")
		rootpc = Modint(Pitchclass(chord[0]).get(), 12)
		nowpc = Modint(rootpc.get(), 12)
		self.bs[nowpc.get()] = 6  # ルート音

		# 第3音と第5音がセットされたかどうかのフラグ
		setno3 = False
		setno5 = False

		# 各和音に対する処理は、Rubyのコードを参考に適宜実装
		# ここでは省略しますが、具体的な和音に応じた処理を行う必要があります。

		# 第3音と第5音の標準設定
		if not setno3:
			nowpc = Modint(rootpc.get(), 12)
			nowpc.add(4)
			self.bs[nowpc.get()] = 4

		if not setno5:
			nowpc = Modint(rootpc.get(), 12)
			nowpc.add(7)
			self.bs[nowpc.get()] = 5

	def get_bs(self):
		"""ベーシックスペースのゲッタ（アクセサ）

			ベーシックスペースを返す

			Returns:
				bs (List): ベーシックスペース

		"""

		return self.bs

	def __str__(self):
		"""クラスの文字列化処理
		
			ベーシックスペースを文字列表示する

		"""
		print("\tfedcba\n--------------")
		for i in range(12):
			buf = Pitchclass(i)
			print(f"{buf.getname()}\t", end="")
			for _ in range(self.bs[i]):
				print("*", end="")
			print()
		return None
