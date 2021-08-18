import discord
import datetime
import asyncio

from discord_slash.utils.manage_components import wait_for_component, create_select, create_select_option, create_actionrow

from discord_slash.context import ComponentContext
from discord_slash import cog_ext, SlashContext

from utils.db import connect_db
from utils.cn import change_name
from utils.json import load_j
from utils.bt import *

from discord.ext import commands

class move(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="이동",
        description="진행 중인 문의 채널을 선택한 카테고리로 이동합니다.",
        guild_ids=[load_j['sub_guild']]
    )
    async def move(self, ctx: SlashContext):
        cur = await connect_db()

        await cur.execute("SELECT Channel FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
        channel = await cur.fetchone()

        if channel == None or ctx.channel.id != channel[0]:
            return await ctx.send(content=f"{ctx.author.mention}, `해당 채널은 문의 채널이 아닙니다!`")

        categorys_list = []
        for categorys in ctx.guild.categories:
            categorys_list_value = create_select_option(label=str(categorys.name), value=str(categorys.id))
            categorys_list.append(categorys_list_value)

        select_category = create_actionrow(
            create_select(
                options=categorys_list,
                placeholder="이동할 카테고리를 선택해주세요.",
                min_values=1,
                max_values=1,
            )
        )
        msg = await ctx.send(content=f"{ctx.author.mention}", components=[select_category, cancel_bt])
        try:
            select_ctx: ComponentContext = await wait_for_component(self.bot, components=[select_category], timeout=30)
        except TimeoutError:
            try:
                return await msg.edit(content=f"{ctx.author.mention}, `제한 시간 안에 응답하지 않아 취소되었습니다.`", components=None, embed=None)
            except discord.errors.Notfound:
                return
        new_category = self.bot.get_channel(id=int(select_ctx.selected_options[0]))

        await ctx.channel.edit(category=new_category)
        await select_ctx.edit_origin(content=f"{ctx.author.mention}, `{new_category.name}`으로 이동하였습니다.", components=None)

def setup(bot):
    bot.add_cog(move(bot))