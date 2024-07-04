"""Music.py

	音楽（和音列）からラティス状の遷移グラフを作成し、和音間距離が最短の解釈を探索する
	
	* Author: Naohiko Yamaguchi
	* Copyright (c) 2024 Naohiko Yamaguchi,IPUT in Tokyo, Japan.
	* License: New BSD License

"""

# 事前に必要な外部モジュールをインポートする
from Chord import Chord
from Delta_chord_calculator import Delta_Chord_calculator

class Node:
	"""Nodeクラス

	グラフを構成するノードを表現するクラス
	Note:
	本クラスは書籍「Java データ構造とアルゴリズム基礎講座」所収のコードをRubyに移植したものである．
	
	Args:
		name (Str): ノード名
		h (Int): ヒューリスティック値
		
	Attributes:
		name (Str): ノード名
		children (List): 子ノードを格納したリスト
		chord_cal (List): 子コードとの距離を格納したリスト
		pointer (Node): 親ノードへのポインタ（参照）
		g (Int): コスト
		h (Int): ヒューリスティック値
		f (Int): 評価値（初期値0）
		hasG (Bool): コスト設定済みフラグ（初期値False）
		hasF (Bool): 評価値設定済みフラグ（初期値False）
	
	"""

	# コンストラクタ
	def __init__(self, name, h):
		self.name = name			#ノード名（引数で指定）
		self.children = []			#子ノード
		self.children_costs = {}	#子ノードのコスト
		self.pointer = None			#親へのポインタ
		self.g = 0					#コスト
		self.h = h					#ヒューリスティック値（引数で指定）
		self.f = 0					#評価値
		self.has_g = False			#コスト設定済みフラグ
		self.has_f = False			#評価値設定済みフラグ

	def get_name(self):
		"""ノード名のゲッタ（アクセサ）

			ノード名を返す

			Returns:
				name (Str): ノード名

		"""
		return self.name
	
	def set_pointer(self, node):
		"""pointerのセッタ（アクセサ）

			pointerに親ノードへの参照を格納する
			
			Args:
				node (Node): 親ノード

		"""
		self.pointer = node
		
	def get_pointer(self):
		"""pointerのゲッタ（アクセサ）

			pointer(親ノード）を返す

			Returns:
				node (Node): 親ノード

		"""
		return self.pointer
		
	def set_g(self, g):
		"""g(コスト)のセッタ（アクセサ）

			gにコストを格納した後、コスト格納済みフラグを立てる
			
			Args:
				g (Int): コスト

		"""
		self.g = g
		self.has_g = True	#コスト設定済みフラグを立てる

	def get_g(self):
		"""g(コスト)のゲッタ（アクセサ）

			g(コスト)を返す

			Returns:
				g (Int): コスト

		"""
		return self.g

	def set_h(self, h):
		"""h(ヒューリスティック値)のセッタ（アクセサ）

			hにヒューリスティック値を格納する
			
			Args:
				h (Int): ヒューリスティック値

		"""
		self.h = h

	def get_h(self):
		"""h(ヒューリスティック値)のゲッタ（アクセサ）

			h(ヒューリスティック値)を返す

			Returns:
				h (Int): ヒューリスティック値

		"""
		return self.h

	def set_f(self, f):
		"""f(評価値)のセッタ（アクセサ）

			fに評価値を格納した後、評価値格納済みフラグを立てる
			
			Args:
				f (Int): 評価値

		"""
		self.f = f
		self.has_f = True	#評価値設定済みフラグを立てる


	def get_f(self):
		"""f(評価値)のゲッタ（アクセサ）

			f(評価値)を返す

			Returns:
				f (Int): 評価値

		"""
		return self.f

	def add_child(self, child, cost):	
		"""子ノードを追加する

			ノードに子ノードを追加する
			
			Args:
				child (Node): 子ノード
				cost (Int): 子ノードへの経路コスト（ノード間距離）

		"""
		self.children.append(child)
		self.children_costs[child] = cost

	def get_children(self):
		"""children(子ノードリスト)のゲッタ（アクセサ）

			children(子ノードリスト)を返す

			Returns:
				children (List): 子ノードリスト

		"""
		return self.children

	def get_cost(self, child):
		"""指定した子ノードへの経路コスト（ノード間距離）を取得

			指定した子ノードへの経路コスト（ノード間距離）を返す
			
			Args:
				child (Node): 子ノード

			Returns:
				children_costs (List): 子ノードリスト

		"""
		return self.children_costs[child]

	def __str__(self):
		"""クラスの文字列化処理
		
			文字列表示する

		"""
		result = f"{self.name}(h:{self.h})"
		if self.has_g:
			result += f"(g:{self.g})"
		if self.has_f:
			result += f"(f:{self.f})"
		return result



class Search:
	"""Searchクラス

		グラフを構成し、探索を行うクラス
		Note:
		本クラスは書籍「Java データ構造とアルゴリズム基礎講座」所収のコードをRubyに移植したものである．

		Attributes:
			node (List): ノード群を格納したリスト
			goal (Node): グラフの終点ノードを示す参照
			start (Node): グラフの始点ノードを示す参照
	
	"""

	def __init__(self):
		self.nodes = []		#ノードリスト
		self.goal = None	#終点ノード
		self.start = None	#始点ノード
		

	def new_node(self, name, heuristic):
		"""グラフにノードを追加する

			指定した子ノードへの経路コスト（ノード間距離）を返す
			
			Args:
				name (Str): ノード名
				heuristic (Int): ヒューリスティック値

			Returns:
				length (Int): ノード数

		"""
		new_node = Node(name, heuristic)
		self.nodes.append(new_node)
		return len(self.nodes) - 1


	def new_branch(self, parent_id, child_id, cost):
		"""ノード間に枝を張る

			指定した子ノード間に経路（枝）を作成する
			
			Args:
				parent_id (Int): 親ノードのノードID
				child_id (Int): 子ノードのノードID
				cost (Int): 枝のコスト（距離）

			Returns:
				length (Int): ノード数

		"""
		self.nodes[parent_id].add_child(self.nodes[child_id], cost)

	# 状態空間の始点ノードと終点ノードを登録
	# == 引数
	# [start_id] 始点ノードとするノードのID
	# [end_id] 終点ノードとするノードのID
	def set_start_goal(self, start_id, end_id):
		"""グラフの始点ノードと終点ノードを指定する

			指定した子ノード間に経路（枝）を作成する
			
			Args:
				start_id (Int): 始点ノードに指定するノードID
				end_id (Int): 終点ノードに指定するノードID

		"""
		self.start = self.nodes[start_id]
		self.goal = self.nodes[end_id]

	#クラスの文字列表記を定義
	def __str__(self):
		"""クラスの文字列化処理
		
			文字列表示する

		"""
		now = self.goal
		result = ""

		while now.get_pointer() is not None:
			result = now.__str__() + " <- " + result
			now = now.get_pointer()

		if now == self.start:
			result = now.__str__() + "\n *Route search was successful.*"
		else:
			result += "*Route search failed."
		return result
	
	
	def aStar(self):
		"""A*アルゴリズムによる最短路探索

			A*（エースター）アルゴリズムによる最短路探索を行う。
			A*アルゴリズムは距離推定値（ヒューリスティック値）を使用して効率的な最短路探索を行うが、
			ヒューリスティック値が指定されていない場合はダイクストラ法に一致する。
			
			グラフ中の各ノードに求めた最短距離を格納する。
			
			Returns:
				success (Bool): 探索成功したか否か

		"""
		open = []
		open.append(self.start)
		
		self.start.set_g(0)
		self.start.set_f(0)
		
		closed = []
		success = False
		step = 0
		
		while True:
			#ステップ数の表示とカウントアップ
			#print("STEP:" + str(step) + "\n")
			step += 1
			
			#これからチェックするノードのリスト
			#print(" OPEN:" + str(open) + "\n")
			#チェックの終わったノードのリスト
			#print(" closed:" + str(closed) + "\n"
			
			if len(open) == 0:
				#もう調べるべきノードが存在しない場合falseを返して終わり
				success = False
				break
			else:
				#調べるべきノードが存在する場合
				#次に調べるノードをopenからnodeへ移す
				node = open[0]
				del open[0]
				
				if node == self.goal:
					success = True
					break
				else:
					#nodeがまだゴールじゃない
					#nodeの子ノードを展開
					children = node.get_children()
					
					#チェックの終わったノードリストにnodeを追加
					closed.append(node)
					
					for i, cnode in enumerate(children):
						#子ノードのi番目をmに移す
						m = cnode
						
						#nodeまでの評価値とnode->mのコストを足したものを
						#gmnとする
						
						gmn = int(node.get_g()) + int(node.get_cost(m))
						
						if m not in open and m not in closed:
							#もしも、子ノードがopenにもclosedにも存在しないなら
							#（つまり未チェックかつチェック予定にも存在しないなら）
							#mのコストとしてgmnを入れる
							m.set_g(gmn)
						
						if m in open:
							#もしも、子ノードがopenに存在するならば
							if gmn < (m.get_g()):
								#今求めた評価値が、計算済みのコストより小さいなら
								#評価値を更新
								m.set_g(gmn)
								#親ノードを更新
								m.set_pointer(node)
							
						
						fmn = gmn + m.get_h()
						
						if m not in open and m not in closed:
							#もしも、子ノードがopenにもclosedにも存在しないなら
							#（つまり未チェックかつチェック予定にも存在しないなら）
							#親ノードを更新
							m.set_pointer(node)
							
							m.set_f(fmn)
							open.append(m)
							
						if m in open and fmn < m.get_f():
							#子ノードがチェック予定にあって評価値がfmnより低いなら
							#評価値をfmnにする
							m.set_f(fmn)
							
							#チェック予定に追加
							open.append(m)
							
							#親ノードを更新
							m.set_pointer(node)
						
						if m in closed and fmn < m.get_f():
							#親ノードを更新
							m.set_pointer(node)
							
							#評価値をfmnにする
							m.set_f(fmn)
							
							#closedにある最初のmを削除
							closed.remove(closed.index(m))
							
							#チェック予定に追加
							open.append(m)
			
			open.sort(key=lambda x: x.get_f())
		return success


# Music
# =プロパティ
# [chordlist] 和音クラス格納行列(Array)
# [chordgraph] 和音探索グラフ(Search)
# = 動作
# TPSの呼び出し元．
class Music:
	"""Musicクラス

	音楽（コード列）を表現し、和音間距離の遷移を分析するクラス
			
	Attributes:
		chordlist  (List): 和音列を表すリスト
		chordgraph (Search): 和音列を分析するためのグラフ
	
	"""

	def __init__(self):
		self.chordlist = []
		self.chordgraph = None
	
	# 和声進行の解釈を行う
	# == 引数
	# [chordsheet] 和音名をカンマ区切りで列挙した文字列(String)
	# == 動作
	# * クラスの初期化を行う。
	# * chordlistの設定
	# * 和音探索グラフの生成
	def explain(self, chordsheet):
		"""和声進行の解釈を行う

			コードネーム列を受け取ってTPS-ExJを用いた和音間距離の分析を行う。
			最短路（合計和音間距離が最も小さくなる解釈）を求めた後、画面に表示する
			
			Args:
				chordsheet (str): コードネーム列を表すテキスト
				

		"""
		#@chordlistを初期化
		self.chordlist = []
		
		#カンマ区切りで渡された和音名列を配列に分割
		chordlistbuf = chordsheet.split(',')
		
		#全ての調パターンを生成
		for cd in range(len(chordlistbuf)):
			self.chordlist.append([])
			for rootpc in range(12):
				self.chordlist[cd].append([chordlistbuf[cd], rootpc, False])
				self.chordlist[cd].append([chordlistbuf[cd], rootpc, True])
		
		#ここから探索グラフの作成
		#グラフクラス生成
		self.chordgraph = Search()
		
		#グラフクラスにノードを登録し，ノード番号を記録
		for i in range(len(self.chordlist)):
			for j in range(len(self.chordlist[i])):
				nodename = self.chordlist[i][j][0] + "/" + str(self.chordlist[i][j][1]) + str(self.chordlist[i][j][2])
				self.chordlist[i][j].append(self.chordgraph.new_node(nodename, 0))
		
		#出発ノード・終点ノードを作成
		startid = self.chordgraph.new_node("START",0)
		endid = self.chordgraph.new_node("END",0)
		
		self.chordgraph.set_start_goal(startid,endid)
		
		#1つ目の和音は，すべて出発ノードとコスト0でリンク作成
		for i in self.chordlist[0]:
			self.chordgraph.new_branch(startid,i[3],0)
		
		
		#最後の和音は，すべて終点ノードとコスト0でリンク作成
		for i in self.chordlist[len(self.chordlist) -1]:
			self.chordgraph.new_branch(i[3],endid,0)
		
		#各枝のコストを計算しながらリンクを作成
		
		tps_cal = Delta_Chord_calculator()
		
		with open("Test_log.txt", 'a') as logfile:
			logfile.write("\n @@ " + str(chordsheet) + " @@@\n")
			print("\n@@@ " + str(chordsheet) + " @@@\n")
		
			#(@chordlist.length) -1回繰り返し
			for i in range(len(self.chordlist) - 1):
				#i番目の和音候補配列の全てから
				for j in self.chordlist[i]:
					#i+1番目の和音候補配列の全てへ
					for k in self.chordlist[i+1]:
						#Chordクラスの生成
						x = Chord(j[0])
						x.set_key(j[1], j[2])
						
						y = Chord(k[0])
						y.set_key(k[1], k[2])
					
						distance = tps_cal.calc_chord_delta(x, y)
						distance_ary = [tps_cal.get_last_delta_chord(), tps_cal.get_last_delta_region(), tps_cal.get_last_delta_basicspace()]
						
						#枝作成
						self.chordgraph.new_branch(j[3], k[3], distance)
					
						logfile.write(str(j) + "\t" + str(distance) + "(C:" + str(distance_ary[0]) + " R:" + str(distance_ary[1]) + " B:" + str(distance_ary[2]) + ")\t" + str(k) + "\n")
				logfile.write("\n")
				
			
			self.chordgraph.aStar()
			
			logfile.write(str(self.chordgraph))
			print(str(self.chordgraph))
		
	def __str__(self):
		"""クラスの文字列化処理
		
			文字列表示する

		"""
		return str(self.chordgraph)



test_music = Music()
test_music.explain("A m 7,D m 7,G 7,C maj7,F maj7,B m 7 -5,E 7,A m 7,A 7,D m 7,G 7,C maj7,A 7,D m 7,G 7,C maj7,B m 7 -5,E 7")
