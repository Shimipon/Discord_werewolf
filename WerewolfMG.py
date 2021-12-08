import Role
import json
import random
import emoji_code as ec

# プレイヤーの情報
class Player:
	def __init__(self, voteID, role = None):
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
		# 投票に使うアルファベット．
		self.VoteID = voteID

	# 夜のアクションのメッセージと能力の対象のリストを返す．
	def Night_Action(self, myID, IDList, day):
		mes = self.Role.night_message(day)
		if mes is None:
			return None, None
		GameConfigJson = open("GameConfig.json","r")
		GameConfig = json.load(GameConfigJson)
		GameRule = GameConfig["Game-Rule"]
		if myID in IDList:
			IDList.remove(myID)
		if self.Role.name == "騎士" and (not GameRule["Same-Guard"]):
			if self.Role.past in IDList:
				IDList.remove(self.Role.past)
		return mes, IDList

	# 生存情報以外の情報をリセットする．
	def reset(self):
		self.FortuneTarget = False
		self.Guard = self.Role.StartGuard()
		self.Voted = False

# ゲームのマネジメント管理をするクラス，discordとのやりとりはせずに必要な情報をとってくる．
class WerewolfMG:
	def __init__(self):
		# プレイヤーの辞書で，IDをキーとしている．役職，プレイヤーステータスの保存を行う．
		self.playerDict = {}

		# 参加しているプレイヤーのIDリスト．これを元に役職を配布したりする．
		self.IDList = []

		# 人狼のプレイヤーのIDリスト．
		self.WolfIDList = []

		# 人間のプレイヤーのIDリスト．
		self.HumanIDList = []

		# 生存しているプレイヤーのIDリスト．
		self.livingIDList = []

		# 現在行われた投票のリスト．「誰が」「誰に」投票したかを保存する．
		self.votedList = []

		# これから行われる投票のリスト．
		self.voteList = []

		# 現在行われた投票の票数の辞書．「誰に」「何票入っている」かを保存する．
		self.voteNumDict = {}

		# 夜の行動が残っている人のIDリスト．
		self.nightActionIDList = []

		# 殺害対象に選ばれた人のIDリスト．複数いる場合はランダムに一人が殺害される．
		self.killTargetList = []

		# 現在の日数
		self.day = 0

		# ゲームの現在のフェイズを表す．
		# 0はゲーム開始前
		# 1は夜のアクションを行うフェイズ
		# 2は議論を行うフェイズ
		# 3は投票を行うフェイズ
		# 4は遺言を残すフェイズ
		self.phase = 0

	# ゲームの情報をリセット．
	def Reset_Game(self):
		self.playerDict.clear()
		self.WolfIDList.clear()
		self.HumanIDList.clear()
		self.livingIDList.clear()
		self.votedList.clear()
		self.nightActionIDList.clear()
		self.voteNumDict.clear()
		self.killTargetList.clear()
		self.day = 0
		return "ゲーム設定をリセットしました"

	# 人数に応じて役職番号のリストを作ってランダムに並べ変えて返す
	def Make_RoleList(self, num):
		GameConfigJson = open("GameConfig.json", "r")
		GameConfig = json.load(GameConfigJson)
		pnum = str(num)
		rList = []
		for r,n in GameConfig[pnum].items():
			for i in range(n):
				rList.append(GameConfig["RoleNumber"][r])
		random.shuffle(rList)
		return rList

	# 参加者をまとめて追加するためのメソッド．変更後の参加者リストを返す．
	def Append_IDList(self, mlist):
		for m in mlist:
			if m not in self.IDList:
				self.IDList.append(m)
		return(self.IDList)

	# 参加者をまとめて削除するためのメソッド．変更後の参加者リストを返す．
	def Remove_IDList(self, mlist):
		for m in mlist:
			if m in self.IDList:
				self.IDList.remove(m)
		return(self.IDList)


	# 参加者を与えられたリストのメンバーに変更するメソッド．変更後の参加者リストを返す．
	def Set_IDList(self, mlist):
		self.IDList.clear()
		for m in mlist:
			self.IDList.append(m)
		return(self.IDList)

	# プレイヤーの辞書を作成する．
	def Make_PlayerDict(self, roleList):
		self.Reset_Game()
		if len(self.IDList) != len(roleList):
			return "役職リストのバグが発生中"
		cList = ec.get_List(len(self.IDList))
		self.phase = 4
		for mem, voteID, rnum in zip(self.IDList, cList, roleList):
			self.livingIDList.append(mem)
			# 役職ナンバーに応じた役職を付与
			r = Role.make_Role(rnum)
			# 人間の場合は人間のIDリストに追加
			if r.human:
				self.HumanIDList.append(mem)
			# そうでない場合は狼のIDリストに追加
			else:
				self.WolfIDList.append(mem)
			vc = ec.get_Code(voteID)
			player = Player(vc, r)
			self.playerDict[mem] = player
		return "プレイヤーのリストを生成しました"

	# 全員の役職のリストを返す．
	def get_PlayerList(self):
		plist = []
		for m in self.playerDict.keys():
			plist.append([m,self.playerDict[m].Role])
		return plist

	# voteID(絵文字)からplayerのdiscordのIDをとってくる
	def get_PlayerID(self, vid):
		for p in self.playerDict.keys():
			if self.playerDict[p].VoteID == vid:
				return p
		return None

	# 対象のプレイヤーを死亡させる関数．
	def Kill(self, player):
		self.playerDict[player].Life = False
		if player in self.livingIDList:
			self.livingIDList.remove(player)
		return 

	# 現在の生存情報からゲームが終了するかを判定する．
	def Check_End(self):
		wolfnum = 0
		for w in self.WolfIDList:
			if self.playerDict[w].Life:
				wolfnum += 1
		if wolfnum == 0:
			if self.Check_Fox():
				return (True,"fox")
			else:
				return (True,"village")
		elif len(self.livingIDList) > wolfnum * 2:
			return (False, None)
		else:
			if self.Check_Fox():
				return (True,"fox")
			else:
				return (True,"werewolf")

	# 現在生存している中に狐がいるかを確認する．
	def Check_Fox(self):
		for m in self.livingIDList:
			if self.playerDict[m].Role.team == "fox":
				return True
		return False

	# 夜の行動リストを作成する．
	def make_NightList(self):
		self.phase = 1
		# 前の履歴が残っていたら，削除する．
		self.nightActionIDList.clear()
		# プレイヤーの対象情報をリセット．
		for plr in self.livingIDList:
			self.playerDict[plr].reset()
		self.killTargetList.clear()

		# 返り値とするリスト．夜の行動があるプレイヤーの「ID」と，
		# そのプレイヤーに送信する「メッセージ」，その行動の対象となるプレイヤーの「IDのリスト」．
		nightList = []
		# 生きているプレイヤー全てについて行動があるか確認．
		for plr in self.livingIDList:
			message, sublist = self.playerDict[plr].Night_Action(plr, self.livingIDList, self.day)
			if message is not None:
				nightList.append((plr,message,sublist))	
		return nightList

	# 初日ランダム白占いを行うためのメソッド．狐と狼以外からランダムに一人を選んで白を出す．
	def random_Fortune(self):
		rlist = []
		teller = 0
		for k,p in zip(self.playerDict.keys(),self.playerDict.values()):
			if p.Role.name == "占い師":
				teller = k 
			elif p.Role.human:
				rlist.append(k)
			if p.Role.team == "fox":
				rlist.remove(k)
		return(teller, random.choice(rlist),"さんは人間でした。")

	# 霊媒師の結果を見るための関数。
	def check_Medium(self):
		voted = None
		message = "昨夜は誰も処刑されませんでした。"
		for p in self.playerDict.keys():
			player = self.playerDict[p]
			if player.Voted:
				voted = p
				if player.Role.human:
					message = "さんは人間でした。"
				else:
					message = "さんは人狼でした。"
		for m in self.livingIDList:
			if self.playerDict[m].Role.name == "霊媒師":
				return (m,voted,message)

	
	# playerの夜の行動をtargetを対象として行う．
	def vote_nightAction(self, player, target):
		if not player in self.nightActionIDList:
			return "あなたのアクションは終了しています。"
		self.nightActionIDList.remove(player)
		RN = self.playerDict[player].Role.name
		if RN == "占い師":
			self.playerDict[player].FortuneTarget = True
			if self.playerDict[target].Role.human:
				return "さんを占った結果は人間でした！"
			else:
				return "さんを占った結果は人狼でした！"
		elif RN == "騎士":
			self.playerDict[player].Role.past = target
			self.playerDict[target].Guard = True
			return "さんを護衛します！"
		elif RN == "人狼":
			self.killTargetList.append(target)
			return "さんを殺害対象に選択しました。"

	# 朝を迎える時の関数．
	# 夜のアクションの結果死亡したプレイヤーのIDのリストを返す．
	def welcome_Morning(self):
		# 夜のアクションが終了しているのか確認．
		if not len(self.nightActionIDList) == 0:
			return ("夜のアクションが終了していません。夜のアクションを終了させてください。", None)
		# 夜のフェイズを終了させる
		self.phase = 2
		# 日付を1日進める
		self.day += 1
		# 返り値とするリスト．死亡した人のIDを保存する．
		death = []
		# 人狼の殺害対象となったプレイヤーが複数いる場合はランダムに決定．
		if len(self.killTargetList) > 1:
			t = random.choice(self.killTargetList)
			self.killTargetList = [t]
		elif len(self.killTargetList) == 0:
			tgt = None
		else:
			tgt = self.killTargetList[0]
		# 殺害対象となったプレイヤーが殺害可能なプレイヤーなら死亡させる．
		if tgt is not None and not self.playerDict[tgt].Guard:
			death.append(tgt)
			self.Kill(tgt)
		# プレイヤーの対象情報をリセット．
		for plr in self.livingIDList:
			self.playerDict[plr].reset()
		self.killTargetList.clear()
		return ("恐ろしい夜が明けて朝がやってきました。", death)

	# 投票する人と，投票対象のリストを生成して返す．
	def make_Vote(self):
		self.phase = 3
		self.voteList.clear()
		self.voteNumDict.clear()
		self.votedList.clear()
		voteMessageList = []
		message = "投票先を選んでください。"
		for plr in self.livingIDList:
			pindex = self.livingIDList.index(plr)
			subList = self.livingIDList[:pindex] + self.livingIDList[pindex+1:]
			voteMessageList.append((plr,message,subList))
			self.voteList.append(plr)
			self.voteNumDict[plr] = 0
		return voteMessageList

	# 決戦投票用の関数．投票する人と，投票対象のリストを生成して返す．
	def make_FinishVote(self, sublist):
		self.voteList.clear()
		self.voteNumDict.clear()
		self.votedList.clear()
		voteMessageList = []
		message = "決戦投票を行います。投票先を選んでください。"
		for plr in self.livingIDList:
			if not plr in sublist:
				voteMessageList.append((plr,message,sublist))
				self.voteList.append(plr)
		for v in sublist:
			self.voteNumDict[v] = 0
		return voteMessageList

	# 投票する．
	def Voting(self, player, voted):
		if not player in self.voteList:
			return "あなたの投票は終了しています。"
		self.voteList.remove(player)
		for pln in self.voteNumDict:
			if pln == voted:
				self.voteNumDict[pln] += 1
				self.votedList.append((player, voted))
				return "さんに投票しました。"

	# 投票結果を返す，最多得票を得たプレイヤーのリストを返す．
	def vote_Result(self):
		if len(self.voteList) != 0:
			return ("投票未完", None, None)
		maxVNum = 0
		mvList = []
		for pln in zip(self.voteNumDict.keys(),self.voteNumDict.values()):
			if pln[1] > maxVNum:
				mvList.clear()
				maxVNum = pln[1]
				mvList.append(pln[0])
			elif pln[1] == maxVNum:
				mvList.append(pln[0])
		if len(mvList) == 0:
			return("バグ", None, None)
		elif len(mvList) == 1:
			self.phase = 4
			self.Kill(mvList[0])
			self.playerDict[mvList[0]].Voted = True
			return("追放完了", mvList[0], None)
		elif len(self.voteNumDict.keys()) == len(self.livingIDList):
			fvlis = self.make_FinishVote(mvList)
			return ("決戦投票", None, fvlis)
		else:
			self.phase = 4
			return("追放失敗", None, None)