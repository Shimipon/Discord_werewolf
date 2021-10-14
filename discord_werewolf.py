import discord
import time
import asyncio
import json
import WerewolfMG

client = discord.Client()
WMG = WerewolfMG.WerewolfMG()

# ユーザー"to"にメッセージ内容"S"のメッセージを送信する
async def DirectMessage(to, S):
	print('Send Message to {0.display_name}'.format(to))
	await to.send(S)

# ゲーム管理側がリアクションを求めているか確認
# async def check_reaction(react_char, user):

async def Make_Private_Vote(to, message, vlist):
	

# 起動時のログ出力
@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

# メッセージが送信された時の動作
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # メンションされたら挨拶する．
    if client.user.mentioned_in(message):
    	print("I was mentioned")
        await message.channel.send('人狼botだよ！よろしく！！')

# botが送ったメッセージにリアクションがついた時の動作
@client.event
async def on_reaction_add(reaction, user):
	if user == client.user:
		return
	# check_reaction(reaction.emoji, user)
	print("I received reaction")
	await reaction.message.channel.send('リアクションありがとう！！')

# 起動するための文
ConfigJson = open("ServerConfig.json", "r")
Config = json.load(ConfigJson)
client.run(Config["token"])