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
intent = discord.Intents.default()
intent.members = True
client = discord.Client(intents = intent)
# wolfChannel = client.get_channel(Config["wolfTextChannel"])
# deadChannel = client.get_channel(Config["deadTextChannel"])


# ユーザー"to"にメッセージ内容"S"のメッセージを送信する
async def DirectMessage(to, S):
	print("Send Message to {0.name}".format(to))
	print("メッセージ文：" + S)
	return await to.send(S)

# userIDからdisplaynameを取得する
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
	rm = rm + "ゲームに参加したい人は✅を押してください。\n参加をやめる人は❎を押してください。"
	return rm

# 指定されたチャンネルに現在のメンバーリストを文字列にして送り，リアクションもつける．
async def send_Member(channel):
	rm = string_Member()
	mes = await channel.send(rm)
	await mes.add_reaction("✅")
	await mes.add_reaction("❎")

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
	for vid, message, vlist in mlist:
		to = client.get_user(vid)
		if to is not None:
			await Make_Private_Vote(to, message, vlist)

def Check_Reaction(vid, user):
	vname = get_DisplayName(vid)
	if WMG.phase == 1 and user in WMG.nightActionIDList:
		return vname + WMG.vote_nightAction(user, vid)
	elif WMG.phase == 3 and user in WMG.voteList:
		return vname + WMG.Voting(user, vid)
	return "あなたのアクションはありません。"

def Get_UserVoiceMember(user):
	channel = user.voice.channel
	return channel.members

# ゲームをスタートするための関数
async def Start_Game(rlist = None):
	if rlist is not None:
		random.shuffle(rlist)
	else:
		rlist = WMG.Make_RoleList(len(WMG.IDList))
	print(rlist)
	print(WMG.Make_PlayerDict(rlist))
	mrlist = WMG.get_PlayerList()
	print(mrlist)
	for m,r in mrlist:
		plr = client.get_user(m)
		if plr is None:
			continue
		message = plr.display_name + "さん、あなたの役職は…\n「" + r + "」です。"
		await DirectMessage(plr, message)


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

	# そのチャンネルのメッセージを100件削除する．
	if message.content == ".dw purge":
		print("メッセージ履歴の削除")
		deleted = await message.channel.purge(limit = 100)
		await message.channel.send("お掃除できたよー！")

	# そのチャンネルのメッセージを特定の件数削除する．
	if message.content.startswith(".dw numpurge"):
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
	if ar == client.user:
		print("I received reaction")
		if WMG.phase == 1 or WMG.phase == 3:
			message = Check_Reaction(WMG.get_PlayerID(reaction.emoji), user.id)
			await DirectMessage(user, message)
		elif WMG.phase == 0:
			async for u in reaction.users():
				if u == client.user:
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
					break

# 起動するための文
client.run(Config["token"])
