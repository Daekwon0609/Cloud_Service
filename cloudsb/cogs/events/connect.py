import discord

from datetime import date
from discord.ext import commands
from utils.check import check_config


class ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        print("Connecting with the server...")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"───────────────────────────────────────\nIn use: Cloud RP\nConnection with the server is complete.")
        print(f"Copyright {date.today().year}. (github: https://github.com/Daekwon0609) all rights reserved.")
        print(f"───────────────────────────────────────\nbot: ({self.bot.user}, {self.bot.user.id})")

        value = await check_config(self.bot)

        if value == True:
            await self.bot.change_presence(activity=discord.Game(name="DM을 통해 문의접수"), status=discord.Status.online)
        else:
            await self.bot.change_presence(activity=discord.Game(name="/설정 대기중"), status=discord.Status.idle)
        
def setup(bot):
    bot.add_cog(ready(bot))