import discord

from datetime import date
from discord.ext import commands
from utils.check import check_config
from discord_slash.utils.manage_commands import remove_all_commands

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
        
        if bool(value):
            await self.bot.change_presence(activity=discord.Game(name=f'/설정 대기'), status=discord.Status.idle)
            print(f'설정 값이 없거나, 찾을 수 없는 채널 및 카테고리가 있어 봇이 중지되었습니다.')
            for check in list(map(str, self.bot.extensions.keys())):
                if check.startswith("cloudsb.cogs.events"):
                    pass
                elif check.endswith(("setup", "refresh")):
                    pass
                else:
                    self.bot.unload_extension(name=check)
        else:
            await self.bot.change_presence(activity=discord.Game(name=f'DM을 통해 문의접수'), status=discord.Status.online)

            

def setup(bot):
    bot.add_cog(ready(bot))