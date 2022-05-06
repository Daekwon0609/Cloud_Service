import discord
import datetime
import os

from natsort import natsorted
from asyncio import TimeoutError

from discord.ext import commands
from interactions.context import ComponentContext

from interactions import SlashContext, cog_ext

from interactions.utils.manage_components import create_select_option, create_actionrow, wait_for_component, create_select

from utils.db import connect_db
from utils.json import load_j
from utils.button_list import cancel_bt
from utils.change import AM_PM

class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="로그",
        description="사용자의 문의 로그들을 확인합니다.",
        guild_ids=[load_j['sub_guild']]
    )
    async def log_command(self, ctx: SlashContext):
        cur = await connect_db()

        await cur.execute("SELECT Channel FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
        channel = await cur.fetchone()

        if channel == None or ctx.channel.id != channel[0]:
            return await ctx.send(content=f"{ctx.author.mention}, `해당 채널은 문의 채널이 아닙니다!`")

        await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
        user_id = await cur.fetchone()

        try: user = await self.bot.fetch_user(user_id=user_id[0])
        except: return await ctx.send(hidden=True, content=f"유저를 찾을 수 없습니다.")

        await cur.execute("SELECT count FROM cloud_log WHERE user_id = ?", (user.id,))
        log_count = await cur.fetchone()

        if log_count == None:
            return await ctx.send(hidden=True, content=f"사용자의 로그를 찾을 수 없습니다. `(사용자: {user})`")
    
        log_list = []
        for file in natsorted(os.listdir("db/log/")):
            if file.startswith(f"{str(user.id)}"):

                file_label = datetime.datetime.fromtimestamp((os.path.getmtime(filename=f'db/log/{file}')))
                AM_PM_value = file_label.strftime('%p')
                file_label_strp = file_label.strftime(f'%Y.%m.%d, {AM_PM(AM_PM_value)} %I:%M')

                file = file.replace(f"{user.id}-", '')
                file = file.replace(".txt", '')

                log_list_value = create_select_option(label=f"{file}", value=f"{file}", description=f"{file_label_strp}")
                log_list.append(log_list_value)
            

        if len(log_list) >= 5:
            select_log = create_actionrow(
                create_select(
                    options=log_list,
                    placeholder="최대 5개, 고른 순서대로 불러옵니다.",
                    min_values=1,
                    max_values=5,
                )
            )
        elif len(log_list) < 5:
            select_log = create_actionrow(
                create_select(
                    options=log_list,
                    placeholder="확인할 로그를 선택해주세요.",
                )
            )
        msg = await ctx.send(content=f"{ctx.author.mention},", components=[select_log, cancel_bt])
        try:
            select_ctx: ComponentContext = await wait_for_component(self.bot, components=[select_log], timeout=30)
        except TimeoutError:
            try:
                return await msg.edit(content=f"{ctx.author.mention}, `제한 시간 안에 응답하지 않아 취소하였습니다.`", components=[], embed=None)
            except discord.errors.Notfound:
                return

        total_file_list = []
        for file_total in select_ctx.selected_options:
            total_file_list.append(discord.File(fp=open(f"db/log/{str(user.id)}-{str(file_total[0])}.txt", "rb"), filename=f"log.txt"))

        await select_ctx.edit_origin(content=f"{ctx.author.mention}, 로그를 불러왔습니다.", components=[], files=total_file_list)

def setup(bot):
    bot.add_cog(log(bot))