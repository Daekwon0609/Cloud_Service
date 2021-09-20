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
        description="문의 채널을 생성합니다.",
        guild_ids=[load_j['sub_guild']],
        options=[
            create_option(
                name="user",
                description="문의 로그를 확인할 ID를 작성해주세요.",
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

        await cur.exeucte("SELECT time, count FROM cloud_log WHERE user_id = ?", (user.id,))
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