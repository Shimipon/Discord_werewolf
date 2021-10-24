import random

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

class Madmate(Role):
	def __init__(self):
		# 人狼陣営
		self.team = "werewolf"
		# 人間
		self.human = True
		# 日本語名
		self.name = "狂人"


class Fox(Role):
	def __init__(self):
		# 村人陣営
		self.team = "fox"
		# 人間
		self.human = True
		# 日本語名
		self.name = "妖狐"

	# 妖狐は人狼には殺害されない．
	def StartGuard(self):
		return True

class Bakery(Role):
	def __init__(self):
		# 村人陣営
		self.team = "village"
		# 人間
		self.human = True
		# 日本語名
		self.name = "パン屋"

#  0.村人
#  1.人狼
#  2.占い師
#  3.霊媒師
#  4.騎士
#  5.狂人
#  6.妖狐
#  7.パン屋

def make_Role(num):
	if num == 1:
		r = Werewolf()
	elif num == 2:
		r = FortuneTeller()
	elif num == 3:
		r = Medium()
	elif num == 4:
		r = Knight()
	elif num == 5:
		r = Madmate()
	elif num == 6:
		r = Fox()
	elif num == 7:
		r = Bakery() 
	else:
		r = Villager()
	return r

# def make_RoleNumList(num):
# 	if 
