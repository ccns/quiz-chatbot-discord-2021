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
        chennel.send('你已經完成題目囉，再 start 一次就可以重新練習了😘')
    else:
        embed = make_prob_embed(prob)
        prob_msg = await channel.send(embed=embed)

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
        user = User(u_name, u_id)
        
        if not user.register():
            await ctx.send('阿北初四了，請聯繫小編處理😵')
            return

        users[u_id] = user
    else: user = users[u_id]

    await bot.get_command('_send_prob').callback(channel, user)

@bot.command(description='get user profile')
async def status(ctx):
    author = ctx.message.author
    u_id = author.id
    
    if u_id not in users:
        await ctx.send('阿北初四了阿北，請先使用 start 註冊帳號🤷')
    else:
        profile = users[u_id].get_status()
        embed = make_status_embed(profile)
        
        await ctx.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id != bot.user.id:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0].to_dict()
        index = embed['title']
        user = users[payload.user_id]
        answer = 0
        
        for emoji in emojis:
            if emoji == payload.emoji.name:
                break
            answer += 1
        
        if answer<4 and users[payload.user_id].check_ans(index, answer):
            await channel.send(get_provoke('true'))
            await bot.get_command('_send_prob').callback(channel, user)
        else:
            await channel.send(get_provoke('false'))

if __name__ == '__main__':
    bot.run(TOKEN)
