import Role
import random
# from Role import Villager #0
# from Role import Werewolf #1
# from Role import FortuneTeller #2
# from Role import Medium #3
# from Role import Knight #4
# from Role import Madmate #5

class Player:
	def __init__(self):
		self.Life = True
		self.FortuneTarget = False
		self.Voted = False
		self.Guard = False
	def reset(self):
		self.FortuneTarget = False
		self.Voted = False
		self.Guard = False
		self.Voted = False


class WerewolfMG:
	def __init__(self):
		# プレイヤーのリストで，IDとプレイヤー情報，
		self.playerList = {}
		self.IDList = []
		self.WolfIDList = []
		self.HumanIDList = []
		self.livingIDList = []
		self.livingHumanIDList = []
		self.voteList = []
		self.nightID = []
		self.voteNumList = []
		self.maxVotePlayers = []
		self.killTarget = []
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
			self.playerList[mem] = [role, player]
		return "プレイヤーのリストを生成しました"

	def Reset_Game(self):
		self.playerList.clear()
		self.IDList.clear()
		self.WolfIDList.clear()
		self.HumanIDList.clear()
		self.livingIDList.clear()
		self.day = 0
		return "ゲーム設定をリセットしました"

	def Kill(self, player):
		self.playerList[player][1].Life = False
		if player in self.livingIDList:
			self.livingIDList.remove(player)
		if player in self.livingHumanIDList:
			self.livingHumanIDList.remove(player)
		return


	def night_List(self):
		self.nightID.clear()
		nightList = []
		for plr in self.livingIDList:
			message = self.playerList[plr][0].night_message()
			if message is not None:
				self.nightID.append(plr)
				if self.playerList[plr][0].name == "人狼":
					subList = self.livingHumanIDList 
					nightList.append((plr,message,subList))
				else:
					subList = self.livingIDList[:self.livingIDList.index(plr)] + self.livingIDList[self.livingIDList.index(plr)+1:] 
					nightList.append((plr,message,subList))	
		return nightList
	
	def night_Action(self, player, target):
		if not player in self.nightID:
			return None
		self.nightID.remove(player)
		RN = self.playerList[player][0].name
		if RN == "占い師":
			self.playerList[player][1].FortuneTarget = True
			if self.playerList[target][0].human:
				return "さんを占った結果は人間でした！"
			else:
				return "さんを占った結果は人狼でした！"
		elif RN == "騎士":
			self.playerList[target][1].Guard = True
			return "さんを護衛します！"
		elif RN == "人狼":
			self.killTarget.append(target)
			return "さんを殺害対象に選択しました。"

	def welcome_Morning(self):
		death = []
		if len(self.killTarget) > 1:
			t = random.choice(self.killTarget)
			self.killTarget = [t]
		tgt = self.killTarget[0]
		if not self.playerList[tgt][1].Guard:
			death.append(tgt)
			self.Kill(tgt)
		for plr in self.livingIDList:
			self.playerList[plr][1].reset()
		self.killTarget.clear()
		return death

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