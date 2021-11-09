import discord
import tools
from discord.ext import commands


class OnStart(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await tools.log(self.client, "NUCAT bot is up")


def setup(client):
    client.add_cog(OnStart(client))
