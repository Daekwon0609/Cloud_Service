import asyncio

from asyncio import TimeoutError

from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.utils.manage_components import wait_for_component

from discord_slash.context import ComponentContext
from discord.ext import commands

from utils.db import connect_db
from utils.bt import *

class button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        if ctx.component_id == "close":
            cur = await connect_db()
            await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
            user_id = await cur.fetchone()

            user = self.bot.get_user(id=user_id[0])

            await cur.execute("DELETE FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))

            await ctx.send(f"{ctx.author.mention}, 문의가 5초 뒤에 종료됩니다.", hidden=True)

            await asyncio.sleep(5)
            await ctx.channel.delete()

            await user.send("`문의가 종료되었습니다.`")
        elif ctx.component_id == "move":
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
            msg = await ctx.send(content=f"{ctx.author.mention},", components=[select_category, cancel_bt])
            try:
                select_ctx: ComponentContext = await wait_for_component(self.bot, components=[select_category, cancel_bt], timeout=30)
            except TimeoutError:
                return await msg.edit(content=f"{ctx.author.mention}, `제한 시간 안에 응답하지 않아 취소되었습니다.`", components=None, embed=None)
            new_category = self.bot.get_channel(id=int(select_ctx.selected_options[0]))

            await ctx.channel.edit(category=new_category)
            await select_ctx.edit_origin(content=f"{ctx.author.mention}, `{new_category.name}`으로 이동하였습니다.", components=None)
        elif ctx.component_id == "cancel":
            return await ctx.edit_origin(content='`진행 중인 작업이 취소되었습니다.`', components=None, embed=None)

def setup(bot):
    bot.add_cog(button(bot))