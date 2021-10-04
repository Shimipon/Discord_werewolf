class Role:
	def __init__(self):
		# 陣営を決める
		self.team = "village"
		# 人外かどうか
		self.human = True
		# 日本語名
		self.jpname = "役職"
	# 夜のアクションがある場合は，アクションの対象のリストを返す
	def make_night_action():
		return
	
class Villager(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.jpname = "村人"

class Werewolf(Role):
	def __init__(self):
		# 人狼陣営
		self.team = "werewolf"
		# 人外
		self.human = False
		# 日本語名
		self.jpname = "人狼"

class FortuneTeller(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.jpname = "占い師"

class Medium(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.jpname = "霊媒師"

class Madmate(Role):
	def __init__(self):
		# 人狼陣営
		self.team = "werewolf"
		# 人間
		self.human = True
		# 日本語名
		self.jpname = "狂人"

class Knight(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.jpname = "騎士"