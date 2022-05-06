import asyncio
import discord

from asyncio import TimeoutError

from interactions.utils.manage_components import create_select, create_select_option, create_actionrow
from interactions.utils.manage_components import wait_for_component

from interactions.context import ComponentContext
from discord.ext import commands

from utils.db import connect_db
from utils.button_list import *
from utils.logging import Add_log
from utils.system_log import log_pr

class button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        if ctx.component_id == "close":
            cur = await connect_db()
            await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
            user_id = await cur.fetchone()

            await cur.execute("SELECT Type FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
            service_type = await cur.fetchone()
            if service_type[0] == 3:
                user = self.bot.get_user(id=user_id[0])

                await ctx.send(f"{ctx.author.mention}, 문의가 5초 뒤에 종료됩니다.")

                await asyncio.sleep(5)

                await Add_log(ctx.channel, user, ctx.author, self.bot, False)
                await cur.execute("DELETE FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
                await log_pr(f"문의 종료: 채널 - {ctx.channel.name} ({ctx.channel.id})")
                await ctx.channel.delete()
            else:
                user = self.bot.get_user(id=user_id[0])

                await ctx.send(f"{ctx.author.mention}, 문의가 5초 뒤에 종료됩니다.")

                await asyncio.sleep(5)

                await Add_log(ctx.channel, user, ctx.author, self.bot, True)
                await cur.execute("DELETE FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
                await log_pr(f"문의 종료: 채널 - {ctx.channel.name} ({ctx.channel.id})")
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
                select_ctx: ComponentContext = await wait_for_component(self.bot, components=[select_category], timeout=30)
            except TimeoutError:
                try:
                    return await msg.edit(content=f"{ctx.author.mention}, `제한 시간 안에 응답하지 않아 취소하였습니다.`", file=None, components=[], embed=None)
                except discord.errors.Notfound:
                    return

            new_category = self.bot.get_channel(id=int(select_ctx.selected_options[0]))

            await ctx.channel.edit(category=new_category)
            await select_ctx.edit_origin(content=f"{ctx.author.mention}, `{new_category.name}`으로 이동하였습니다.", components=[])
        elif ctx.component_id == "cancel":
            return await ctx.edit_origin(content=f'{ctx.author.mention}, `진행 중인 작업을 취소하였습니다.`', file=None, components=[], embed=None)
        elif ctx.component_id == "service_queue_cancel":
            cur = await connect_db()
            await cur.execute("SELECT User_id FROM cloud_service WHERE User_id = ?", (ctx.author.id,))
            queue_cancel = await cur.fetchone()

            if queue_cancel == None:
                return await ctx.edit_origin(content=f'{ctx.author.mention}, `진행 중인 문의 선택을 취소하였습니다.`', file=None, components=[], embed=None)
            else:
                await cur.execute("DELETE FROM cloud_service WHERE User_id = ?", (ctx.author.id,))
                return await ctx.edit_origin(content=f'{ctx.author.mention}, `진행 중인 문의 선택을 취소하였습니다.`', file=None, components=[], embed=None)
        elif ctx.component_id == "report_category" or ctx.component_id == "support_category" or ctx.component_id == "server_category":
            cur = await connect_db()

            await cur.execute("SELECT Type FROM cloud_service WHERE User_id = ?", (ctx.author.id,))
            queue_service = await cur.fetchone()

            if queue_service == None:
                return await ctx.edit_origin(content=f'{ctx.author.mention}, `비 정상적인 행동이 감지되어 취소되었습니다.`', file=None, components=[], embed=None)
            elif queue_service[0] == 2:
                await cur.execute("DELETE FROM cloud_service WHERE User_id = ?", (ctx.author.id,))
                return await ctx.edit_origin(content=f'{ctx.author.mention}, `비 정상적인 오류가 감지되어 취소되었습니다.`', file=None, components=[], embed=None)

def setup(bot):
    bot.add_cog(button(bot))