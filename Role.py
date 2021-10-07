class Role:
	def __init__(self):
		# 陣営を決める
		self.team = "village"
		# 人外かどうか
		self.human = True
		# 日本語名
		self.name = "役職"
	def night_message(self):
		return None
		
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
	def night_message(self):
		return "護衛対象を選択してください。"