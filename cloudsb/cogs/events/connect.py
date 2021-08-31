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
            print(f'설정 값이 없거나, 찾을 수 없는 채널 및 카테고리가 있어 프로세스가 중지되었습니다.')
            print("/설정 을 모두 완료한 후에 프로세스를 다시 시작해주세요.")
            
            for check in list(map(str, self.bot.extensions.keys())):
                if check.endswith(("setup", "error")):
                    continue
                else:
                    self.bot.unload_extension(name=check)
            
            print(f'\n임시 활성화된 Extensions: {", ".join(list(map(str, self.bot.extensions.keys())))}')
            print(f'문제 항목: {", ".join(value)}')
        else:
            await self.bot.change_presence(activity=discord.Game(name=f'DM을 통해 문의접수'), status=discord.Status.online)

def setup(bot):
    bot.add_cog(ready(bot))