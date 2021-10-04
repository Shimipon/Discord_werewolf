import Role
# from Role import Villager #0
# from Role import Werewolf #1
# from Role import FortuneTeller #2
# from Role import Medium #3
# from Role import Knight #4
# from Role import Madmate #5

class Player:
	def __init__(self):
		self.Life = True
		self.KillTarget = False
		self.FortuneTarget = False
		self.Voted = False
		self.Guard = False

class WerewolfMG:
	def __init__(self):
		self.playerList = []
		self.day = 0

	def Make_PlayerList(self, memberList, roleList):
		if len(memberList) != len(roleList):
			return "役職リストのバグが発生中"
		for mem, rnum in zip(memberList, roleList):
			if rnum == 1:
				role = Role.Werewolf()
			elif rnum == 2:
				role = Role.FortuneTeller()
			elif rnum == 3:
				role = Role.Medium()
			elif rnum == 4:
				role = Role.Knight()
			elif rnum == 5:
				role = Role.Madmate()
			else:
				role = Role.Villager()
			player = Player()
			self.playerList.append((mem, role, player))
		return "プレイヤーのリストを生成しました"

	def Reset_PlayerList(self):
		self.playerList.clear()
		return "プレイヤーリストをリセットしました"
