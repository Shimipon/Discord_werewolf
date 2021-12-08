import discord
import time
import asyncio
import json
import emoji_code as ec
import WerewolfMG
import re

WMG = WerewolfMG.WerewolfMG()
ConfigJson = open("ServerConfig.json", "r")
Config = json.load(ConfigJson)
GameConfigJson = open("GameConfig.json","r")
GameConfig = json.load(GameConfigJson)
GameRule = GameConfig["Game-Rule"]
intent = discord.Intents.default()
intent.members = True
client = discord.Client(intents = intent)
# wolfChannel = client.get_channel(Config["wolfTextChannel"])
# deadChannel = client.get_channel(Config["deadTextChannel"])

# ユーザー"to"にメッセージ内容"S"のメッセージを送信する
async def DirectMessage(to, S):
	if S == "":
		return
	if S is None:
		return
	print("Send Message to {0.name}".format(to))
	print("メッセージ文：" + S)
	return await to.send(S)

def get_DisplayName(ID):
	user = client.get_user(ID)
	name = ""
	if user is None:
		name = "????" + str(ID)
	else:
		name = user.display_name
	return name

# 現在の参加者を文字列にしたものを返す，メッセージを編集するのに便利
def string_Member():
	rm = "現在の参加者のリストです。\n"
	for m in WMG.IDList:
		rm = rm + get_DisplayName(m) + "さん\n"
	rm = rm + "以上です！\n"
	if len(WMG.IDList) == 0:
		rm = "現在参加者はいません！\n"
	rm = rm + "ゲームに参加したい人は✅を押してください。\n参加をやめる人は❎を押してください。\n"
	rm = rm + "ゲームを始める時は🆗を押してください。"
	return rm

# 指定されたチャンネルに現在のメンバーリストを文字列にして送り，リアクションもつける．
async def send_Member(channel):
	rm = string_Member()
	mes = await channel.send(rm)
	await mes.add_reaction("✅")
	await mes.add_reaction("❎")
	await mes.add_reaction("🆗")

# user型のリストからIDのリストを生成する
def get_IDList(members):
	lis = []
	for m in members:
		lis.append(m.id)
	return lis

# DMで投票を行う
async def Make_Private_Vote(to, message, vlist):
	for v in vlist:
		vID = WMG.playerDict[v].VoteID
		message = message + "\n" + vID + ". " + get_DisplayName(v) + "さん"
	message = message + "\nの中から選択してください！"
	sended = await DirectMessage(to, message)
	for v in vlist:
		vID = WMG.playerDict[v].VoteID
		await sended.add_reaction(vID)

# チャットチャンネルで投票を行う
# async def Make_Public_Vote(to, message, vlist):

# 受け取ったリストを使って投票を行う．IDが見つからない時はランダムに投票する．
async def All_Private_Vote(mlist):
	for uid, message, vlist in mlist:
		to = client.get_user(uid)
		if to is not None:
			await Make_Private_Vote(to, message, vlist)
		else:
			WMG.Voting(uid, random.choice(vlist))

# リアクションによる投票を行っているかどうか確認する。
def Check_Reaction(vid, user):
	vname = get_DisplayName(vid)
	if WMG.phase == 1 and user in WMG.nightActionIDList:
		return vname + WMG.vote_nightAction(user, vid)
	elif WMG.phase == 3 and user in WMG.voteList:
		return vname + WMG.Voting(user, vid)
	return "あなたのアクションは終了しています。"

# 引数にしたuserが参加しているボイスチャンネルを返す．
def Get_UserVoiceMember(user):
	channel = user.voice.channel
	return channel.members

# リアクションインスタンスを受け取りbotが同じリアクションをつけているか確認する．つけているならTrueを返す．
async def If_BotReaction(reaction):
	async for u in reaction.users():
		if u == client.user:
			return True
			# print("TRUE")
	return False
	# print("False!")

# ゲームをスタートするための関数．
async def Start_Game(rlist = None):
	if rlist is not None:
		random.shuffle(rlist)
	else:
		rlist = WMG.Make_RoleList(len(WMG.IDList))
	# print(rlist)
	print(WMG.Make_PlayerDict(rlist))
	mrlist = WMG.get_PlayerList()
	# print(mrlist)
	for m,r in mrlist:
		plr = client.get_user(m)
		if plr is None:
			continue
		message = plr.display_name + "さん、あなたの役職は…\n「" + r.name + "」です。"
		await DirectMessage(plr, message)

# リストの人全員に霊界を見せる。
async def Permit_Deadchat(ulist):
	c = client.get_channel(Config["deadTextChannel"])
	for user in ulist:
		await c.set_permissions(user, read_messages=True, send_messages=True)

# 死んでる人だけ霊界を見せる。
async def PermitDead_Deadchat():
	dlis = []
	for mid in WMG.IDList:
		if not WMG.playerDict[mid].Life:
			dlis.append(client.get_user(mid))
	await Permit_Deadchat(dlis)

# リストの人全員に狼チャットを見せる。
async def Permit_Wolfchat(ulist):
	c = client.get_channel(Config["wolfTextChannel"])
	for user in ulist:
		await c.set_permissions(user, read_messages=True, send_messages=True)

# 狼の人だけ狼チャットを見せる。
async def PermitWolf_Wolfchat():
	wlis = []
	for wid in WMG.WolfIDList:
		wlis.append(client.get_user(wid))
	await Permit_Wolfchat(wlis)

# リストの人全員に狼チャットを見せるが，書き込みはできなくする．
async def Read_Wolfchat(ulist):
	c = client.get_channel(Config["wolfTextChannel"])
	for user in ulist:
		await c.set_permissions(user, read_messages=True, send_messages=False)

# 狼の人だけ狼チャットを見せるが，書き込みはできなくする．
async def ReadWolf_Wolfchat(ulist):
	wlis = []
	for wid in WMG.WolfIDList:
		wlis.append(client.get_user(wid))
	await Read_Wolfchat(wlis)

# リストの人全員に霊界を見えなくする。
async def Forbid_Deadchat(ulist):
	c = client.get_channel(Config["deadTextChannel"])
	for user in ulist:
		await c.set_permissions(user, read_messages=False, send_messages=False)

# リストの人全員に狼チャットを見えなくする。
async def Forbid_Wolfchat(ulist):
	c = client.get_channel(Config["wolfTextChannel"])
	for user in ulist:
		await c.set_permissions(user, read_messages=False, send_messages=False)

# 参加者全員に霊界と狼チャットを見えなくする。
async def ForbidMember_chat():
	mlis = []
	for mid in WMG.IDList:
		mlis.append(client.get_user(mid))
	await Forbid_Wolfchat(mlis)
	await Forbid_Deadchat(mlis)

# ゲームが終了した際に呼び出される。勝利した陣営を知らせて、役職を公開する。
async def End_Message(ch,team):
	mes1 = "ゲームが終了しました。\n"
	if team == "werewolf":
		mes1 = mes1 + "わおーーーーーん！人狼陣営の勝利です！！"
	elif team == "fox":
		mes1 = mes1 + "こんこん！狐陣営の勝利です！！"
	elif team == "village":
		mes1 = mes1 + "これで村は安全だ！村人陣営の勝利です！！"
	await ch.send(mes1)
	mes2 = "みなさんの役職を発表します。\n"
	plis = WMG.get_PlayerList()
	for pid,r in plis:
		mes2 = mes2 + get_DisplayName(pid) + "さん⇒「" + r.name + "」\n"
	mes2 = mes2 + "お疲れ様でした！"
	await ch.send(mes2)

# ゲームを進めるための関数．
async def Go_Game():
	pc = client.get_channel(Config["gameTextChannel"])
	if WMG.phase == 0:
		ok = await pc.send("ゲームを開始します！参加者の方々にDMで役職をお知らせします！\n全員役職を確認してください！")
		await Start_Game()
		await ForbidMember_chat()
		await PermitWolf_Wolfchat()
		await ok.add_reaction("🆗")

	elif WMG.phase == 1:
		(mes, death) = WMG.welcome_Morning()
		if death is None:
			await pc.send(mes)
			ok = await pc.send("議論を開始する際は🆗を押してください。")
			await ok.add_reaction("🆗")
		else:
			await pc.send(mes)
			await asyncio.sleep(1)
			await pc.send("昨晩亡くなった人は…")
			await asyncio.sleep(1)
			m = ""
			for uid in death:
				u = client.get_user(uid)
				m = m + u.display_name + "さん\n"
			if len(death) == 0:
				m = m + "いません"
			m = m + "でした。"
			await pc.send(m)
			await asyncio.sleep(1)
			chk, team = WMG.Check_End()
			if chk:
				await End_Message(pc,team)
				return
			await ReadWolf_Wolfchat()
			await PermitDead_Deadchat()
			ok = await pc.send(str(WMG.day) + "日目の昼の議論を開始してください。\n議論を終了する際は🆗を押してください。")
			await ok.add_reaction("🆗")

	elif WMG.phase == 2:
		await pc.send("これから投票を行います。皆様に投票するためのメッセージをダイレクトメッセージで送信します。\nリアクションボタンを使い投票してください！")
		await All_Private_Vote(WMG.make_Vote())
		ok = await pc.send("投票結果を確認するためには🆗を押してください。")
		await ok.add_reaction("🆗")
	
	elif WMG.phase == 3:
		mes, ex, fvlis = WMG.vote_Result()
		if mes == "投票未完":
			ok = await pc.send("まだ投票が完了していません。投票が完了したら🆗を押してください。")
			await ok.add_reaction("🆗")
		if mes == "決戦投票":
			m = "投票の結果、最多票の人が複数いたため決戦投票を行います。最多票だったのは以下の人たちです。\n"
			for v in fvlis[0][2]:
				m = m + get_DisplayName(v) + "\n"
			m = m + "投票対象以外の方々に皆様に投票するためのメッセージをダイレクトメッセージで送信します。"
			await pc.send(m)
			await All_Private_Vote(fvlis)
			ok = await pc.send("投票結果を確認するためには🆗を押してください。")
			await ok.add_reaction("🆗")
		if mes == "追放完了":
			pc.send("投票の結果、追放されたのは…")
			await asyncio.sleep(2)
			await pc.send(get_DisplayName(ex) + "さんでした。")
			await asyncio.sleep(1)
			chk, team = WMG.Check_End()
			if chk:
				await End_Message(pc,team)
				return
			m2 = get_DisplayName(ex) + "さんは遺言を残すことができます。\n"	
			m2 = m2 + "遺言を残し終えたら🆗を押してください。"
			ok = await pc.send(m2)
			await ok.add_reaction("🆗")
		if mes == "追放失敗":
			m = "決選投票の結果、再び同票になったため処刑を行いませんでした。\n"
			m = m + "まもなく夜が訪れます、準備ができましたら🆗を押してください。"
			ok = await pc.send(m)
			await ok.add_reaction("🆗")

	elif WMG.phase == 4:
		await pc.send(str(WMG.day) + "日目の夜がやってきました。夜のアクションがある方にはアクションのためのダイレクトメッセージを送信します。")
		await PermitDead_Deadchat()
		if WMG.day == 0:
			if GameRule["Random-Fortune"]:
				tel, tgt, mes1 = WMG.random_Fortune()
				if client.get_user(tel) is not None:
					await DirectMessage(client.get_user(tel), get_DisplayName(tgt) + mes1)
			for w in WMG.WolfIDList:
				await DirectMessage(client.get_user(w), "夜の間だけは人狼テキストチャットに書き込みができます！昼になると読むことしかできません！")
		else:
			med, vtd, mes = WMG.check_Medium()
			if vtd is None:
				await DirectMessage(client.get_user(med), mes)
			else:
				await DirectMessage(client.get_user(med), get_DisplayName(vtd) + mes)
		await All_Private_Vote(WMG.make_NightList())
		ok = await pc.send("みなさんの目が覚めたころに🆗を押してください。")
		await ok.add_reaction("🆗")


# リリース時は以下を削除

# 投票機能のテスト
# async def voteTest(to):
# 	message = "投票機能のテストを行います！"
# 	memberList = [to.id,1,2,3,4,5,6,7]
# 	# rlist = WMG.Make_RoleList(8)
# 	rlist = [1,0,0,0,0,0,0,0]
# 	print(WMG.Append_IDList(memberList))
# 	print(WMG.Make_PlayerDict(rlist))
# 	print(WMG.get_PlayerList())
# 	WMG.night = False
# 	await All_Private_Vote(WMG.make_Vote())

# # ゲーム開始のテスト
# async def startTest(to):
# 	print("ゲームを始めるテストを行います！")
# 	await DirectMessage(to, "ゲームを始めるテストを行います！")
# 	memberList = [to.id,1,2,3,4,5,6,7]
# 	print(WMG.Append_IDList(memberList))
# 	await Start_Game()

# 権限管理のテスト
# async def permissionTest1():
# 	to = client.get_user(Config["TestUser"])
# 	c = client.get_channel(Config["wolfTextChannel"])
# 	await c.set_permissions(to, read_messages=True, send_messages=True)

# async def permissionTest2():
# 	to = client.get_user(Config["TestUser"])
# 	c = client.get_channel(Config["wolfTextChannel"])
# 	await c.set_permissions(to, read_messages=False, send_messages=False)

# async def permissionTest1(to):
# 	# c = client.get_channel(Config["wolfTextChannel"])
# 	wolfChannel = client.get_channel(Config["wolfTextChannel"])
# 	await wolfChannel.set_permissions(to, read_messages=True, send_messages=True)

# async def permissionTest2(to):
# 	# c = client.get_channel(Config["wolfTextChannel"])
# 	wolfChannel = client.get_channel(Config["wolfTextChannel"])
# 	await wolfChannel.set_permissions(to, read_messages=False, send_messages=False)

# ここまで削除

# 起動時のログ出力
@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))

# メッセージが送信された時の動作
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	# メンションされたら挨拶する．
	if client.user.mentioned_in(message):
		print("I was mentioned")
		await message.channel.send("人狼botだよ！よろしく！！")
		
	# メンバー設定を始めるためのコマンド．
	if message.content == ".dw member":
		print("参加者確認and設定")
		await send_Member(message.channel)

	# コマンドを送信した人が参加しているボイチャを取得し，そこに参加している人達をゲームの参加者に設定しなおす．
	if message.content == ".dw member v":
		print("ボイスチャンネルを元に参加者を設定する．")
		user = message.author
		if user.voice is None:
			await message.channel.send(user.display_name + "さんはボイスチャットに参加していません。")
			await send_Member(message.channel)
		else:
			vc = user.voice.channel
			await message.channel.send(vc.name + "で通話しているプレイヤーを参加者にします。")
			WMG.Set_IDList(get_IDList(vc.members))
			await send_Member(message.channel)

	# そのチャンネルのメッセージを上限100件削除する．
	if message.content == ".dw purge":
		print("メッセージ履歴の削除")
		deleted = await message.channel.purge(limit = 100)
		await message.channel.send("お掃除できたよー！")

	# そのチャンネルのメッセージを特定の件数削除する．
	if message.content.startswith(".dw numpurge") or message.content.startswith(".dw eat"):
		print("特定件数のメッセージ履歴の削除")
		m = re.findall(r'[0-9]+', message.content)
		if len(m) > 0:
			num = int(m[0])
			deleted = await message.channel.purge(limit = num+1)
			await message.channel.send(m[0] + "件のメッセージを食べちゃった！")
		else:
			await message.channel.send('削除するメッセージの件数を一緒に送ってください。')

	# 以下はテスト関数を呼び出す用．
	# if message.content == ".dw ptest1":
	# 	await permissionTest1(message.author)
	# if message.content == ".dw ptest2":
	# 	await permissionTest2(message.author)
	# if message.content == ".dw voteTest":
	# 	await voteTest(message.author)
	# if message.content == ".dw startTest":
	# 	await startTest(message.author)

# botが送ったメッセージにリアクションがついた時の動作
@client.event
async def on_reaction_add(reaction, user):
	ar = reaction.message.author
	if user == client.user:
		return
	elif ar == client.user:
		if reaction.emoji == "🆗":
			await Go_Game()
		elif WMG.phase == 1 or WMG.phase == 3:
			mes = Check_Reaction(WMG.get_PlayerID(reaction.emoji), user.id)
			await reaction.message.channel.send(mes)
		elif WMG.phase == 0:
			if reaction.emoji == "✅":
				mes = user.display_name + "さんをメンバーに追加します。\n"
				WMG.Append_IDList([user.id])
				mes = mes + string_Member()
				await reaction.message.edit(content = mes)
			elif reaction.emoji == "❎":
				mes = user.display_name + "さんをメンバーから削除します...またね...。\n"
				WMG.Remove_IDList([user.id])
				mes = mes + string_Member()
				await reaction.message.edit(content = mes)
		await reaction.remove(user)
			
# 起動するための文
client.run(Config["token"])
