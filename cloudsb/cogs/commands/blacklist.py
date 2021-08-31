import discord
import datetime

from discord_slash.utils.manage_commands import create_permission, create_option
from discord_slash.model import SlashCommandPermissionType
from discord_slash import SlashContext, cog_ext

from utils.json import load_j
from utils.db import connect_db 

from discord.ext import commands

class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="블랙리스트",
        description="고객센터 블랙리스트를 지정합니다.",
        default_permission=False,
        options=[
            create_option(
                name="user",
                description="블랙리스트를 지정할 유저를 선택해주세요.",
                option_type=6,
                required=True
            )
        ],
        permissions={
            load_j['sub_guild']: [
                create_permission(
                    id=load_j['blacklist_role'],
                    id_type=SlashCommandPermissionType.ROLE,
                    permission=True
                )
            ]
        }
    )
    async def blacklist(self, ctx: SlashContext, user: discord.User):
        async with connect_db as cur:
            await cur.execute("SELECT user_id FROM cloud_blacklist WHERE user_id = ?", (user.id,))
            user_same = await cur.fetchone()

            if user_same == None:
                pass
            elif user_same[0] == user.id:
                return await ctx.send(hidden=True, content=f"이미 블랙리스트 유저이므로 취소되었습니다. `(유저 아이디: {user.id})`")
            
            await cur.execute("INSERT INTO cloud_blacklist(user_id, time) values(?, ?)", (user.id, int(datetime.datetime.now().timestamp())))

            blacklist_emb = discord.Embed(title="BLACKLIST - COMMAND", description=f"등록 시간: <t:{int(datetime.datetime.now().timestamp())}>\n\n유저: {user.mention} (**{user.id}**)")
            
            await ctx.send(content=f"{ctx.author.mention},", embed=blacklist_emb)

def setup(bot):
    bot.add_cog(blacklist(bot))
