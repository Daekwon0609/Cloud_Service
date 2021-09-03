import discord

from utils.json import load_j
from utils.db import connect_db
from discord.ext import commands

from discord_slash.model import SlashCommandPermissionType

from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_permission, create_option

class create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="생성",
        description="문의 채널을 생성합니다.",
        options=[
            create_option(
                name="user",
                description="문의 채널을 생성할 유저를 선택합니다.",
                option_type=6,
                required=True
            )
        ],
        permissions={
            load_j['sub_guild']: [
                create_permission(
                    id=load_j['setup_role'],
                    id_type=SlashCommandPermissionType.ROLE,
                    permission=True
                )
            ]
        }
    )
    async def create_thred(self, ctx: SlashContext, user: discord.User):
        cur = await connect_db()

        await ctx.send(f"{user.id}, {user} 귀찮다.")

def setup(bot):
    bot.add_cog(create(bot))

