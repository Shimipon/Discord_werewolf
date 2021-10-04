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
		self.IDList = []
		self.WolfIDList = []
		self.HumanIDList = []
		self.day = 0

	def Make_PlayerList(self, memberList, roleList):
		if len(memberList) != len(roleList):
			return "役職リストのバグが発生中"
		for mem, rnum in zip(memberList, roleList):
			self.IDList.append(mem)
			if rnum == 1:
				role = Role.Werewolf()
				self.WolfIDList.append(mem)
			elif rnum == 2:
				role = Role.FortuneTeller()
				self.HumanIDList.append(mem)
			elif rnum == 3:
				role = Role.Medium()
				self.HumanIDList.append(mem)
			elif rnum == 4:
				role = Role.Knight()
				self.HumanIDList.append(mem)
			elif rnum == 5:
				role = Role.Madmate()
				self.HumanIDList.append(mem)
			else:
				role = Role.Villager()
				self.HumanIDList.append(mem)
			player = Player()
			self.playerList.append((mem, role, player))
		return "プレイヤーのリストを生成しました"

	def Reset_PlayerList(self):
		self.playerList.clear()
		self.IDList.clear()
		return "プレイヤーリストをリセットしました"

	def night_List(self):
		voteList = []
		for plr in self.playerList:
			if plr[1].name == "占い師":
				message = "占い対象を選択してください。"
				subList = self.IDList[:self.IDList.index(plr[0])] + self.IDList[self.IDList.index(plr[0])+1:] 
				voteList.append((plr[0],message,subList))
			elif plr[1].name == "騎士":
				message = "護衛対象を選択してください。"
				subList = self.IDList[:self.IDList.index(plr[0])] + self.IDList[self.IDList.index(plr[0])+1:] 
				voteList.append((plr[0],message,subList))
			elif plr[1].name == "人狼":
				message = "殺害する対象を選択してください。"
				subList = self.HumanIDList 
				voteList.append((plr[0],message,subList))
		return voteList