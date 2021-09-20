import discord
import datetime

from discord_slash.model import ButtonStyle

from discord.ext import commands
from discord_slash.context import ComponentContext

from discord_slash import SlashContext, cog_ext

from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_select_option, create_actionrow, wait_for_component, create_select

from utils.db import connect_db
from utils.json import load_j
from utils.button_list import cancel_bt

class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="로그",
        description="사용자의 문의 로그들을 확인합니다.",
        guild_ids=[load_j['sub_guild']],
    )
    async def log_command(self, ctx: SlashContext, user):
        cur = await connect_db()

        await cur.execute("SELECT Channel FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
        channel = await cur.fetchone()

        if channel == None or ctx.channel.id != channel[0]:
            return await ctx.send(content=f"{ctx.author.mention}, `해당 채널은 문의 채널이 아닙니다!`")

        await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
        user_id = await cur.fetchone()

        try: user = await self.bot.fetch_user(user_id=user_id[0])
        except: return await ctx.send(hidden=True, content="유저를 찾을 수 없습니다.")

        await cur.execute("SELECT time, count FROM cloud_log WHERE user_id = ?", (user.id,))
        log_count = await cur.fetchall()
        
        log_list = []
        for log in log_count:
            log_list_value = create_select_option(label=f"<:t{log[0]}:F>", value=f"{log[1]}")
            log_list.append(log_list_value)

        select_category = create_actionrow(
            create_select(
                options=log_list,
                placeholder="확인할 로그를 선택해주세요. (최대 5개)",
                min_values=1,
                max_values=5,
            )
        )
        msg = await ctx.send(content=f"{ctx.author.mention},", components=[select_category, cancel_bt])
        try:
            select_ctx: ComponentContext = await wait_for_component(self.bot, components=[select_category], timeout=30)
        except TimeoutError:
            try:
                return await msg.edit(content=f"{ctx.author.mention}, `제한 시간 안에 응답하지 않아 취소되었습니다.`", components=None, embed=None)
            except discord.errors.Notfound:
                return

        file = open(f"db/log/{str(user.id)}-{str(select_ctx.selected_options[0])}.txt","rb")

        await select_ctx.edit_origin(content=f"{ctx.author.mention}, 로그 {select_ctx.selected_options[0]}개를 불러왔습니다.", components=None, file=discord.File(fp=file, name="log"))

def setup(bot):
    bot.add_cog(log(bot))