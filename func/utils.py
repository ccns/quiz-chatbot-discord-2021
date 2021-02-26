import discord
from typing import Dict

def make_prob_embed(prob):
    content: str = ""
    color: Dict[str, int] = {
        'Eazy': 0x1fff00,
        'Medium': 0xe8ff00,
        'Hard': 0xff0000
    }

    for i in range(0, 4):
        content += '{}. {}\n\n'.format(
                chr(ord('A')+i),
                prob['options'][i]
        )

    embed = discord.Embed(
            title = prob['description'],
            author = prob['author'],
            color = color[prob['level']],
            description = content
    )
    embed.set_footer(text = '標籤: ' + prob['domain'])

    return embed

def make_status_embed(profile):
    color = 0x00ffff
    print(profile)
    content = '分數: {}\n\n 平台: {}'.format(
            profile['correct_count'],
            profile['platform']
    )
    embed = discord.Embed(
            title = profile['name'],
            description = content,
            color = color
    )

    return embed
