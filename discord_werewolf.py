import discord
import time
import asyncio

client = discord.Client()



# ユーザー"to"にメッセージ内容"S"のメッセージを送信する
async def DirectMessage(to, S):
	print('Send Message to {0.display_name}'.format(to))
	await to.send(S)

# ゲーム管理側がリアクションを求めているか確認
def check_reaction(react_char, user):



# 起動時のログ出力
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_reaction_add(reaction, user)
	if user == client.user:
        return
    check_reaction(reaction.emoji, user)
    return