import discord
import time
import asyncio
import json
import emoji_code
import WerewolfMG

WMG = WerewolfMG.WerewolfMG()
ConfigJson = open("ServerConfig.json", "r")
Config = json.load(ConfigJson)
ec = emoji_code.Emoji_Code()
intent = discord.Intents.default()
intent.members = True
client = discord.Client(intents = intent)
# ユーザー"to"にメッセージ内容"S"のメッセージを送信する
async def DirectMessage(to, S):
	print("Send Message to {0.name}".format(to))
	return await to.send(S)

# ゲーム管理側がリアクションを求めているか確認
# async def check_reaction(react_char, user):

# DMで投票を行う
async def Make_Private_Vote(to, message, vlist):
	for v in vlist:
		vID = WMG.playerList[v].VoteID
		vuser = client.get_user(v)
		vname = vuser.display_name
		message = message + "\n" + vID + "." + vname + "さん"
	message = message + "\nの中から選択してください！"
	sended = await DirectMessage(to, message)
	for v in vlist:
		vID = WMG.playerList[v].VoteID
		await sended.add_reaction(vID)
# チャットチャンネルで投票を行う
# async def Make_Public_Vote(to, message, vlist):

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

# botが送ったメッセージにリアクションがついた時の動作
@client.event
async def on_reaction_add(reaction, user):
	if user == client.user:
		return
	# check_reaction(reaction.emoji, user)
	if reaction.message.author == client.user:
		print("I received reaction")
		Isend = await reaction.message.channel.send(ec.code["B"] + "リアクションありがとう！！")
		await Isend.add_reaction(ec.code["A"])
		await DirectMessage(user,"リアクションほんとにありがとう！！")

# 起動するための文
client.run(Config["token"])