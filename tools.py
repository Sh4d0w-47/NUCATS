import re
import discord
import os
from discord.ext import commands


async def log(client, value):
    l = client.get_channel(int(os.environ["log_channel"]))
    await l.send(str(value))

async def checkUniversityUsername(m):
    if len(m) != 8:
        return False
    regex = r'^([A-C|a-c])\d{7}$'
    if re.match(regex, m):
        return True
    else:
        return False

async def userInputDM(client, ctx, str):
    while True:
        msg = await client.wait_for("message")
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if msg.content.lower() == str.lower() or re.match(str, msg.content.lower()):
                break
            else:
                await ctx.author.send("Invalid input, please try again")
    return msg
