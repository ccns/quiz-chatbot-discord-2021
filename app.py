import os
import discord

from typing import Dict
from func.user import User
from func.logger import logger
from discord.ext import commands
from func.config import HOST, TOKEN
from func.backend import get_provoke
from func.utils import make_prob_embed, make_status_embed

bot = commands.Bot(command_prefix='/')
platform = 'Discord'
emojis = list()
users: Dict[str, User] = {}
emojis = ["\U0001f1e6", "\U0001f1e7", "\U0001f1e8", "\U0001f1e9"]

@bot.event
async def on_ready():
    logger.info('Do U want to meow with {}?'.format(bot.user))

@bot.command(description='send problem')
async def _send_prob(channel, user):
    prob = user.get_problem()

    if not prob:
        await user.dc_user.send('感謝您遊玩我們準備的 Chatbot Q&A！\n我們的期初社團大會將在 3/11 (四) 晚上 19:00 在資訊系館 4201 教室舉行，詳細聚會資訊與教室位置圖請查詢最近 FB 粉絲專頁動態。歡迎來現場與我們聊天，也可以先加入 Discord 聊天群及關注粉絲專頁歐～\n\n[Discord Group] https://discord.ccns.io/\n[FB Fan-page] https://www.facebook.com/ncku.ccns')
    else:
        embed = make_prob_embed(prob)
        prob_msg = await user.dc_user.send(embed=embed)

        for emoji in emojis:
            await prob_msg.add_reaction(emoji)

@bot.command(description='start message')
async def start(ctx):
    global users

    author = ctx.message.author
    channel = ctx.message.channel
    u_name = author.name
    u_id = author.id

    if u_id not in users:
        user = User(u_name, u_id, author)
        
        if not user.register():
            await user.dc_user.send('阿北初四了，請聯繫小編處理😵')
            return

        await user.dc_user.send("```Hello World!\n歡迎參加 CCNS Chatbot Q&A 競賽，我們準備了數十題連出題者都不一定能答對的題目，前三名高分的玩家我們會在 3/11 (四) 期初社團大會進行頒獎！\n歡情嘗試各種方法取得高分，包含但不限於查 Stackoverflow、問資訊系教授、通靈以及熬夜刷題。```")
        users[u_id] = user
    else: user = users[u_id]

    await bot.get_command('_send_prob').callback(channel, user)

@bot.command(description='get user profile')
async def status(ctx):
    author = ctx.message.author
    u_id = author.id
    
    if u_id not in users:
        await author.send('阿北初四了阿北，請先使用 start 註冊帳號🤷')
    else:
        profile = users[u_id].get_status()
        embed = make_status_embed(profile)
        
        await author.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    u_id = payload.user_id
    channel = await bot.fetch_channel(payload.channel_id)
    _user = await bot.fetch_user(u_id)

    if u_id != bot.user.id:
        if u_id not in users:
            await _user.send('發生了點小問題，請輸入 start 重新啟動😵')
            logger.warning('something wrong happend, user id not in users list')
            return
        
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0].to_dict()
        index = embed['title']
        user = users[u_id]
        answer = 0
        
        for emoji in emojis:
            if emoji == payload.emoji.name:
                break
            answer += 1
        
        correctness = users[u_id].check_ans(index, answer)
        
        if correctness == "Error Index":
            await user.dc_user.send('發生了點小問題，請重新 start 😒')
            return
        
        if correctness == "Error":
            await user.dc_user.send('你已經答過題目了，不要再重複回答😡')
            return

        if answer<4 and correctness:
            await user.dc_user.send('👌 ' + get_provoke('true'))
        else:
            await user.dc_user.send('👎 ' + get_provoke('false'))
        
        await bot.get_command('_send_prob').callback(channel, user)

if __name__ == '__main__':
    bot.run(TOKEN)
