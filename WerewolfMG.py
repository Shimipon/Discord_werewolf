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
		# プレイヤーのリストで，IDとプレイヤー情報，
		self.playerList = []
		self.IDList = []
		self.WolfIDList = []
		self.HumanIDList = []
		self.livingIDList = []
		self.livingHumanIDList = []
		self.voteList = []
		self.voteNumList = []
		self.maxVotePlayers = []
		self.day = 0

	def Make_PlayerList(self, memberList, roleList):
		if len(memberList) != len(roleList):
			return "役職リストのバグが発生中"
		for mem, rnum in zip(memberList, roleList):
			self.IDList.append(mem)
			self.livingIDList.append(mem)
			# 役職ナンバーに応じた役職を付与
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
			# 人間の場合は人間のIDリストに追加
			if role.human:
				self.HumanIDList.append(mem)
				self.livingHumanIDList.append(mem)
			# そうでない場合は狼のIDリストに追加
			else:
				self.WolfIDList.append(mem)
			player = Player()
			self.playerList.append((mem, role, player))
		return "プレイヤーのリストを生成しました"

	def Reset_Game(self):
		self.playerList.clear()
		self.IDList.clear()
		self.WolfIDList.clear()
		self.HumanIDList.clear()
		self.livingIDList.clear()
		self.day = 0
		return "プレイヤーリストをリセットしました"

	def night_List(self):
		nightList = []
		for plr in self.playerList:
			if plr[1].name == "占い師":
				message = "占い対象を選択してください。"
				subList = self.livingIDList[:self.livingIDList.index(plr[0])] + self.livingIDList[self.livingIDList.index(plr[0])+1:] 
				nightList.append((plr[0],message,subList))
			elif plr[1].name == "騎士":
				message = "護衛対象を選択してください"
				subList = self.livingIDList[:self.livingIDList.index(plr[0])] + self.livingIDList[self.livingIDList.index(plr[0])+1:] 
				nightList.append((plr[0],message,subList))
			elif plr[1].name == "人狼":
				message = "殺害する対象を選択してください。"
				subList = self.livingHumanIDList 
				nightList.append((plr[0],message,subList))
		return nightList
	
	#def night_Action(self, player, target):
	#	for plr in self.playerList:


	def make_Vote(self):
		voteMessageList = []
		for plr in self.livingIDList:
			message = "投票対象を選択してください。"
			subList = self.livingIDList[:self.livingIDList.index(plr)] + self.livingIDList[self.livingIDList.index(plr)+1:]
			voteMessageList.append((plr,message,subList))
			self.voteNumList.append([plr, 0])
		return voteMessageList

	def Voting(self, player, voted):
		for pln in self.voteNumList:
			if pln[0] == voted:
				pln[1] = pln[1] + 1
				self.voteList.append((player, voted))
				return

	def voteResult(self):
		if len(self.voteList) != len(self.livingIDList):
			return ("投票が完了していません。", [])
		maxVNum = 0
		for pln in self.voteNumList:
			if pln[1] > maxVNum:
				self.maxVotePlayers.clear()
				maxVNum = pln[1]
				self.maxVotePlayers.append(pln[0])
			elif pln[1] == maxVNum:
				self.maxVotePlayers.append(pln[0])
		return ("投票が完了しました。", self.maxVotePlayers)






