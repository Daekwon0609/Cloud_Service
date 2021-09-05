import discord

from utils.json import load_j
from utils.db import connect_db
from discord.ext import commands

from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

class create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="생성",
        description="문의 채널을 생성합니다.",
        guild_ids=[load_j['sub_guild']],
        options=[
            create_option(
                name="user",
                description="문의 채널을 생성할 유저의 ID를 작성해주세요.",
                option_type=3,
                required=True
            )
        ]
    )
    async def create_thred(self, ctx: SlashContext, user):
        try: user = int(user)
        except: return await ctx.send(hidden=True, content="유저의 ID를 적어주세요!")
        
        cur = await connect_db()

        try: user = await self.bot.fetch_user(user_id=user)
        except: return await ctx.send(hidden=True, content="유저를 찾을 수 없습니다.")
        await ctx.send(f"{user.id}, {user}")

def setup(bot):
    bot.add_cog(create(bot))

