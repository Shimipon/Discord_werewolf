import Role
import random

# プレイヤーの情報
class Player:
	def __init__(self, role = None):
		# 生存しているか否か．
		self.Life = True
		# 占いの対象になっているか否か．
		self.FortuneTarget = False
		# 前日に投票で殺されたか否か．
		self.Voted = False
		# プレイヤーの役職，指定された役職が無ければ村人にする．
		if role is None:
			self.Role = Role.Villager()
		else:
			self.Role = role
		# 騎士の護衛対象になっている，若しくは人狼に殺されなくなっているか否か．
		self.Guard = role.StartGuard()
	# 生存情報以外の情報をリセットする．
	def reset(self):
		self.FortuneTarget = False
		self.Guard = self.role.StartGuard()
		self.Voted = False

# ゲームのマネジメント管理をするクラス，discordとのやりとりはせずに必要な情報をとってくる．
class WerewolfMG:
	def __init__(self):
		# プレイヤーの辞書で，IDをキーとしている．役職，プレイヤーステータスの保存を行う．
		self.playerList = {}
		# 参加しているプレイヤーのIDリスト．
		self.IDList = []
		# 人狼のプレイヤーのIDリスト．
		self.WolfIDList = []
		# 人間のプレイヤーのIDリスト．
		self.HumanIDList = []
		# 生存しているプレイヤーのIDリスト．
		self.livingIDList = []
		# 生存している人間のプレイヤーのリスト．
		self.livingHumanIDList = []
		# 現在行われた投票のリスト．「誰が」「誰に」投票したかを保存する．
		self.voteList = []
		# 現在行われた投票の票数の辞書．「誰に」「何票入っている」かを保存する．
		self.voteNumList = {}
		# 得票が最も多かったプレイヤーのリスト．決戦投票の際に使う．
		self.maxVotePlayers = []
		# 夜の行動が残っている人のIDリスト．
		self.nightActionID = []
		# 殺害対象に選ばれた人のIDリスト．複数いる場合はランダムに一人が殺害される．
		self.killTarget = []
		# 現在の日数
		self.day = 1

	# プレイヤーのリストを作成する．
	def Make_PlayerList(self, memberList, roleList):
		if len(memberList) != len(roleList):
			return "役職リストのバグが発生中"
		for mem, rnum in zip(memberList, roleList):
			self.IDList.append(mem)
			self.livingIDList.append(mem)
			# 役職ナンバーに応じた役職を付与
			if rnum == 1:
				r = Role.Werewolf()
			elif rnum == 2:
				r = Role.FortuneTeller()
			elif rnum == 3:
				r = Role.Medium()
			elif rnum == 4:
				r = Role.Knight()
			elif rnum == 5:
				r = Role.Madmate()
			else:
				r = Role.Villager()
			# 人間の場合は人間のIDリストに追加
			if r.human:
				self.HumanIDList.append(mem)
				self.livingHumanIDList.append(mem)
			# そうでない場合は狼のIDリストに追加
			else:
				self.WolfIDList.append(mem)
			player = Player(r)
			self.playerList[mem] = player
		return "プレイヤーのリストを生成しました"

	# ゲームの情報をリセット．
	def Reset_Game(self):
		self.playerList.clear()
		self.IDList.clear()
		self.WolfIDList.clear()
		self.HumanIDList.clear()
		self.livingIDList.clear()
		self.livingHumanIDList.clear()
		self.voteList.clear()
		self.nightActionID.clear()
		self.voteNumList.clear()
		self.maxVotePlayers.clear()
		self.killTarget.clear()
		self.day = 0
		return "ゲーム設定をリセットしました"

	# 対象のプレイヤーを死亡させる関数．
	def Kill(self, player):
		self.playerList[player].Life = False
		if player in self.livingIDList:
			self.livingIDList.remove(player)
		if player in self.livingHumanIDList:
			self.livingHumanIDList.remove(player)
		return

	# 夜の行動リストを作成する．
	def night_List(self):
		# 前の履歴が残っていたら，削除する．
		self.nightActionID.clear()
		# 返り値とするリスト．夜の行動があるプレイヤーの「ID」と，
		# そのプレイヤーに送信する「メッセージ」，その行動の対象となるプレイヤーの「IDのリスト」．
		nightList = []
		# 生きているプレイヤー全てについて行動があるか確認．
		for plr in self.livingIDList:
			message = self.playerList[plr].Role.night_message()
			if message is not None:
				self.nightActionID.append(plr)
				if self.playerList[plr].Role.name == "人狼":
					subList = self.livingHumanIDList 
					nightList.append((plr,message,subList))
				else:
					subList = self.livingIDList[:self.livingIDList.index(plr)] + self.livingIDList[self.livingIDList.index(plr)+1:] 
					nightList.append((plr,message,subList))	
		return nightList
	
	# playerの夜の行動をtargetを対象として行う．
	def night_Action(self, player, target):
		if not player in self.nightActionID:
			return None
		self.nightActionID.remove(player)
		RN = self.playerList[player].Role.name
		if RN == "占い師":
			self.playerList[player].FortuneTarget = True
			if self.playerList[target].Role.human:
				return "さんを占った結果は人間でした！"
			else:
				return "さんを占った結果は人狼でした！"
		elif RN == "騎士":
			self.playerList[target]Guard = True
			return "さんを護衛します！"
		elif RN == "人狼":
			self.killTarget.append(target)
			return "さんを殺害対象に選択しました。"

	# 朝を迎える時の関数．
	# 夜のアクションの結果死亡したプレイヤーのIDのリストを返す．
	def welcome_Morning(self):
		# 返り値とするリスト．死亡した人のIDを保存する．
		death = []
		# 夜のアクションが終了しているのか確認．
		if not len(nightActionID) == 0:
			return "夜のアクションが終了していません。\n夜のアクションを終了させてください。" 
		# 人狼の殺害対象となったプレイヤーが複数いる場合はランダムに決定．
		if len(self.killTarget) > 1:
			t = random.choice(self.killTarget)
			self.killTarget = [t]
		tgt = self.killTarget[0]
		# 殺害対象となったプレイヤーが殺害可能なプレイヤーなら死亡させる．
		if not self.playerList[tgt].Guard:
			death.append(tgt)
			self.Kill(tgt)
		# プレイヤーの対象情報をリセット．
		for plr in self.livingIDList:
			self.playerList[plr].reset()
		self.killTarget.clear()
		return death

	# 投票する人と，投票対象のリストを生成返す．
	def make_Vote(self):
		voteMessageList = []
		for plr in self.livingIDList:
			message = "投票対象を選択してください。"
			subList = self.livingIDList[:self.livingIDList.index(plr)] + self.livingIDList[self.livingIDList.index(plr)+1:]
			voteMessageList.append((plr,message,subList))
			self.voteNumList[plr] = 0
		return voteMessageList

	# 投票する．
	def Voting(self, player, voted):
		for pln in self.voteNumList:
			if pln == voted:
				self.voteNumList[pln] += 1
				self.voteList.append((player, voted))
				return

	# 投票結果を返す，最多得票
	def vote_Result(self):
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
		self.voteNumList.clear()
		self.voteList.clear()
		return ("投票が完了しました。", self.maxVotePlayers)