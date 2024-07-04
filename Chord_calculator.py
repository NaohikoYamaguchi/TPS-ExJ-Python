"""Chord_calculator.py

	TPSのChord距離を算出するモジュール
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""

# 事前に必要な外部モジュールをインポートする
from Modint import Modint
from Chord import Chord
from Basicspace_calculator import BasicspaceCalculator

class ChordCalculator:
	"""ChordCalculatorクラス

		TPSのコード距離を算出する
				
		Attributes:
			chord_a (Chord): 算出元のコードクラス
			chord_b (Chord): 算出元のコードクラス
			chordcircle_a(list): chord_aの「和音の五度圏」
			chordcircle_b(list): chord_bの「和音の五度圏」
			pivot_a(list): chord_aの「ピヴォットコード」
			pivot_b(list): chord_bの「ピヴォットコード」
			delta(Int): コード距離

	"""
	
	CHORD_DISTANCE_UNMEASURABLE = 99
	"""CHORD_DISTANCE_UNMEASURABLE
	
		コード距離をを測定できなかった時に返す（十分大きな）定数＝無限遠

	"""

	def __init__(self):
		self.chord_a = None
		self.chord_b = None
		self.chordcircle_a = None
		self.chordcircle_b = None
		self.pivot_a = None
		self.pivot_b = None
		self.delta = None

	def calc_chord(self, chord_a, chord_b):
		"""コード距離を算出する

			与えられた2つのコードクラスから、距離を算出する

			Args:
				chord_a (Chord): 算出元のコードクラス
				chord_b (Chord): 算出元のコードクラス
			
			Returns:
				delta (Int): コード距離

		"""
		
		#引数をプロパティに記録する
		self.chord_a = chord_a
		self.chord_b = chord_b

		#ピヴォット候補配列を求める
		#ピヴォットが必要ない場合（つまり与えられたコードがダイアトニックの場合）与えられたコード名がそのまま入る
		
		#@chord_aのchord circleの中で@chord_aのコードネームを探索する．
		self.pivot_a = self.pickup_pivotlist(self.chord_a)
		self.pivot_b = self.pickup_pivotlist(self.chord_b)
		
		#@chord_bのchord circleの中で@chord_bのコードネームを探索する．
		self.chordcircle_a = self.make_chordcircle(self.chord_a.get_root(), self.chord_a.get_minorflag())
		self.chordcircle_b = self.make_chordcircle(self.chord_b.get_root(), self.chord_b.get_minorflag())
		
		#結果格納用リストの初期化
		result = []
		
		#@chord_aのchord circleの中に@chord_bのピヴォットコード名が存在するか．
		#全てのピヴォットコードの組み合わせを探索
		#現在探索対象となっているchord_aのピヴォットコード名がpivot_a_nowcheck
		#現在探索対象となっているchord_bのピヴォットコード名がpivot_b_nowcheck
		for pivot_a_nowcheck in self.pivot_a[0]:
			for pivot_b_nowcheck in self.pivot_b[0]:
				if pivot_b_nowcheck in self.chordcircle_a:
					#見つかった
					
					#以下，和音の5度圏上の距離を算出する
					#chord_aの和音の5度上でpivot_a_nowcheckが存在する位置を，距離測定の起点base_positionとする
					base_position = Modint(self.chordcircle_a.index(pivot_a_nowcheck), len(self.chordcircle_a))
					
					#距離計測カウンタをリセット
					counter = 0
					
					#和音の5度圏を時計回りに数える
					for i in range(len(self.chordcircle_a)):
						if self.chordcircle_a[base_position.get()] == pivot_b_nowcheck:
							#pivot_b_nowcheckと一致したら数えるのをやめる
							break
						else:
							#pivot_b_nowcheckと一致しなかったらもう1ステップ時計回りに進む
							base_position.add(1)
							counter += 1

					#もしも得られた距離が和音の5度圏の長さの半分より大きければ，
					#反時計回りに探索した方が早かった事になるので，反時計回りの距離に修正する
					if counter > (len(self.chordcircle_a) / 2.0):
						counter = len(self.chordcircle_a) - counter
					
					#和音の5度圏からピヴォットコードとしての場合，外に伸びた枝の分を追加する
					if self.pivot_a[1]:
						counter += 1
					if self.pivot_b[1]:
						counter += 1

					#得られた距離を結果格納Arrayにプッシュする
					result.append(counter)
				else:
					#見つからなかった→chord距離算出不可
					#十分に大きな値を結果としてプッシュする
					result.append(self.CHORD_DISTANCE_UNMEASURABLE)
		
		#@chord_bのchord circleの中に@chord_aのピヴォットコード名が存在するか．
		#全てのピヴォットコードの組み合わせを探索
		#現在探索対象となっているchord_aのピヴォットコード名がpivot_a_nowcheck
		#現在探索対象となっているchord_bのピヴォットコード名がpivot_b_nowcheck
		for pivot_b_nowcheck in self.pivot_b[0]:
			for pivot_a_nowcheck in self.pivot_a[0]:
				if pivot_a_nowcheck in self.chordcircle_b:
					#見つかった
					
					#以下，和音の5度圏上の距離を算出する
					#chord_bの和音の5度上でpivot_b_nowcheckが存在する位置を，距離測定の起点base_positionとする
					base_position = Modint(self.chordcircle_b.index(pivot_b_nowcheck), len(self.chordcircle_b))
					
					#距離計測カウンタをリセット
					counter = 0
					
					#和音の5度圏を時計回りに数える
					for i in range(len(self.chordcircle_b)):
						if self.chordcircle_b[base_position.get()] == pivot_a_nowcheck:
							#pivot_a_nowcheckと一致したら数えるのをやめる
							break
						else:
							#pivot_a_nowcheckと一致しなかったらもう1ステップ時計回りに進む
							base_position.add(1)
							counter += 1

					#もしも得られた距離が和音の5度圏の長さの半分より大きければ，
					#反時計回りに探索した方が早かった事になるので，反時計回りの距離に修正する
					if counter > (len(self.chordcircle_b) / 2.0):
						counter = len(self.chordcircle_b) - counter

					#和音の5度圏からピヴォットコードとしての場合，外に伸びた枝の分を追加する
					if self.pivot_a[1]:
						counter += 1
					if self.pivot_b[1]:
						counter += 1

					#得られた距離を結果格納Arrayにプッシュする
					result.append(counter)
				else:
					#見つからなかった→chord距離算出不可
					#十分に大きな値を結果としてプッシュする
					result.append(self.CHORD_DISTANCE_UNMEASURABLE)

		#結果格納用Arrayのうち，最小のものを出力する
		minimum = result[0]		#初期値として先頭を代入
		for i in result:
			if minimum > i:
				minimum = i

		self.delta = minimum
		return self.delta
		
	def make_chordcircle(self,root, is_minor):
		"""五度圏を表す配列を生成する

			調のルート、長調/短調フラグから、調の五度圏を生成する。

			Args:
				root (int): 調のルート
				is_minor (Boolean): 長調/短調フラグ(True->短調,False->長調)

		"""
		chordcircle = []
		
		if is_minor == False:
			# 長調のとき
			#このルックアップテーブルは『コード進行スタイルブック』p.182に基づく．
			major_lookup = [
				["C", "E m", "G", "B m -5", "D m", "F", "A m"],
				["Db", "F m", "Ab", "C m -5", "Eb m", "Gb", "Bb m"],
				["D","F# m","A","C# m -5","E m","G","B m"],
				["Eb","G m","Bb","D m -5","F m","Ab","C m"],
				["E","G# m","B","D# m -5","F# m","A","C# m"],
				["F","A m","C","E m -5","G m","Bb","D m"],
				["Gb","Bb m","Db","F m -5","Ab m","B","Eb m"],
				["G","B m","D","F# m -5","A m","C","E m"],
				["Ab","C m","Eb","G m -5","Bb m","Db","F m"],
				["A","C# m","E","G# m -5","B m","D","F# m"],
				["Bb","D m","F","A m -5","C m","Eb","G m"],
				["B","D m","F#","A# m -5","C# m","E","G# m"]
			]
			chordcircle = major_lookup[root]
		else:
			# 短調のとき
			minor_lookup = [
				["C m", "Eb", "G m", "Bb", "D m -5", "F m", "Ab"],
				["C# m", "E", "G# m", "B", "D# m -5", "F# m", "A"],
				["D m","F","A m","C","E m -5","G m","Bb"],
				["Eb m","Gb","Bb m","Db","F m -5","Ab m","B"],
				["Eb m","G","B m","D","F# m -5","A m","C"],
				["F m","Ab","C m","Eb","G m -5","Bb m","Db"],
				["F# m","A","C# m","E","G# m -5","B m","D"],
				["G m","Bb","D m","F","A m -5","C m","Eb"],
				["G# m","B","D# m","F#","A# m -5","C# m","E"],
				["A m","C","E m","G","B m -5","D m","F"],
				["Bb m","Db","F m","Ab","C m -5","Eb m","Gb"],
				["B m","D","F# m","A","C# m -5","E m","G"]
			]
			chordcircle = minor_lookup[root]
		
		return chordcircle
	
	def pickup_pivotlist(self,chord):
		"""（ピヴォット）候補配列を求める

			和音の5度圏の中から，ベーシックスペース距離が最も近い和音（ピヴォット）候補配列を求める

			Args:
				chord (Code): ピヴォットを求めるコード
				
			Return:
				pivot（List)（戻り値pivot[0]はピヴォット候補コード名リスト，pivot[1]はピヴォットが必要か否かのフラグ）

		"""
	
		#chordのchord circleの中でchordのコードネームを探索する．
		#chordの置かれた調に対応するchordcircleを生成
		chordcircle = [self.make_chordcircle(chord.get_root(), chord.get_minorflag()), []]
		
		#ピヴォット候補格納配列の生成
		#ピヴォット候補は複数ある可能性があるので配列形式
		pivot = []

		if chord.get_chordname() in chordcircle[0]:
			#chord circleにコードネームが含まれている
			#ピヴォットはいらない．そのままコード名を格納する．
			need_pivot_flag = False
			pivot = [chord.get_chordname()]
		else:
			#chord circleにコードネームが含まれていない
			#basicspace関数を使ってピヴォットコードを探す．
			need_pivot_flag = True
			
			#ベーシックスペース算出クラス生成
			bcalc = BasicspaceCalculator()

			#全てのダイアトニックコードとaのコードのベーシックスペース距離を算出する
			for i, diatonic_chord_name in enumerate(chordcircle[0]):
				#比較対象コードを取り出してChordクラスを生成
				diatonic = Chord(diatonic_chord_name)
				diatonic.set_key(chord.get_root(), chord.get_minorflag())

				#ベーシックスペース距離を算出して格納
				chordcircle[1].append(bcalc.calc_basicspace(diatonic, chord))

			#ベーシックスペース距離の最小値を求める
			minimum = min(chordcircle[1])		#初期値として先頭をベーシックスペース距離を代入
			
			#最小値の距離を持ったダイアトニックコード名をピヴォット候補として取り出す
			for i, distance in enumerate(chordcircle[1]):
				if distance == minimum:
					pivot.append(chordcircle[0][i])

		return [pivot, need_pivot_flag]
		

	def get_lastdelta(self):
		"""コード距離のゲッタ（アクセサ）

			最後に求めたコード距離を返す

			Returns:
				delta (Int): コード距離

		"""
		return self.delta