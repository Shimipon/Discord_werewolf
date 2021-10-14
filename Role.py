class Role:
	def __init__(self):
		# 陣営を決める
		self.team = "village"
		# 人外かどうか
		self.human = True
		# 日本語名
		self.name = "役職"
	# 夜の行動がある場合はメッセージを返す．
	def night_message(self):
		return None
	# 狼に殺されない役職の場合はTrueにする．
	def StartGuard(self):
		return False
		
class Villager(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.name = "村人"
		
class Werewolf(Role):
	def __init__(self):
		# 人狼陣営
		self.team = "werewolf"
		# 人外
		self.human = False
		# 日本語名
		self.name = "人狼"
	# 殺害対象を選択する．
	def night_message(self):
		return "殺害対象を選択してください。"
		
class FortuneTeller(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.name = "占い師"
	# 占い対象を選択する．
	def night_message(self):
		return "占い対象を選択してください。"

class Medium(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.name = "霊媒師"
				
class Madmate(Role):
	def __init__(self):
		# 人狼陣営
		self.team = "werewolf"
		# 人間
		self.human = True
		# 日本語名
		self.name = "狂人"
			
class Knight(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.name = "騎士"
	# 護衛対象を選択する．
	def night_message(self):
		return "護衛対象を選択してください。"