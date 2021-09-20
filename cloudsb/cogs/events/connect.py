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
        value = await check_config(self.bot)
        
        if bool(value):
            await self.bot.change_presence(activity=discord.Game(name=f'/���� ���'), status=discord.Status.idle)
            print(f'���� ���� ���ų�, ã�� �� ���� ä�� �� ī�װ��� �־� ���μ����� �����Ǿ����ϴ�.')
            print('���ڵ� ������ "/����"�� ��� �Ϸ��� �Ŀ� ���μ����� �ٽ� �������ּ���.')
            
            for check in list(map(str, self.bot.extensions.keys())):
                if check.endswith(("setup", "error")):
                    continue
                else:
                    self.bot.unload_extension(name=check)
            
            print(f'\n�ӽ� Ȱ��ȭ�� Extensions: {", ".join(list(map(str, self.bot.extensions.keys())))}')
            print(f'���� �׸�: {", ".join(value)}')
        else:
            await self.bot.change_presence(activity=discord.Game(name=f'DM�� ���� ��������'), status=discord.Status.online)

            print(f"������������������������������������������������������������������������������\nIn use: Cloud RP\nConnection with the server is complete.")
            print(f"Copyright {date.today().year}. (github: https://github.com/Daekwon0609) all rights reserved.")
            print(f"������������������������������������������������������������������������������\nbot: ({self.bot.user}, {self.bot.user.id})")