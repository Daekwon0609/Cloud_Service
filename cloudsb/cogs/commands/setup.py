import discord

from discord_slash.utils.manage_commands import create_option, create_permission, create_choice
from discord_slash.utils.manage_components import create_button, create_actionrow

from discord_slash.model import ButtonStyle, SlashCommandPermissionType, ContextMenuType

from discord_slash import cog_ext, SlashContext
from discord_slash.context import MenuContext

from utils.db import connect_db
from utils.cn import change_name
from utils.json import load_j

from discord.ext import commands


class setupa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="설정",
        description="고객센터 시스템을 설정합니다.",
        default_permission=False,
        options=[
            create_option(
                name="categories",
                description="설정할 카테고리의 종류를 선택해주세요.",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name="서버문의",
                        value="server_category"
                    ),
                    create_choice(
                        name="후원문의",
                        value="support_category"
                    ),
                    create_choice(
                        name="신고하기",
                        value="report_category" 
                    )
                ]
            ),
            create_option(
                name="category",
                description="설정할 카테고리의 이름을 작성하거나, 선택해주세요. (ex. #카테고리 이름)",
                option_type=7,
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
    async def add_button(self, ctx: SlashContext, categories: str, category: str):
        if str(category.type) != "category":
            return await ctx.send(hidden=True, content="카테고리 타입으로 다시 선택해주세요!")

        category = self.bot.get_channel(id=category.id)

        cur = await connect_db()

        await cur.execute("SELECT Category FROM cloud_setup WHERE Category = ? and Type = ?", (category.id, categories))
        same_id = await cur.fetchone()

        if same_id[0] == category.id:
            categories = change_name(categories)
            return await ctx.send(hidden=True, content=f"중복된 내용이므로 취소되었습니다. `(종류: {categories}, 아이디: {category.id})`")

        await cur.execute("UPDATE cloud_setup SET Category = ? WHERE Type = ?", (category.id, categories))  

        categories = change_name(categories)

        setup_emb = discord.Embed(title="SETUP - COMMAND", description=f"`/setup_info` 로 전체 확인이 가능합니다.\n\n바꾼 카테고리 종류: **[{categories}]**\n바꾼 카테고리 아이디: **{category.id}**")
        
        await ctx.send(content=f"{ctx.author.mention},", embed=setup_emb)

    @cog_ext.cog_slash(
        name="정보",
        description="고객센터 봇의 설정된 정보를 볼 수 있습니다.",
        default_permission=False,
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
    async def setupinfo(self, ctx: SlashContext):
        setup_emb = discord.Embed(title="SETUP - INFO", description="`/정보` 으로 다시 설정할 수 있습니다.")

        cur = await connect_db()
                
        await cur.execute("SELECT Category, Type FROM cloud_setup")
        list_categ = await cur.fetchall()

        for categ in list_categ:
            type = change_name(categ[1])
            id = self.bot.get_channel(id=categ[0])

            try:
                channel = id.id
            except AttributeError:
                setup_emb.add_field(name=f"카테고리 종류: [{type}]", value=f"**아이디 :** *N/A*", inline=False)
            else:
                setup_emb.add_field(name=f"카테고리 종류: [{type}]", value=f"**아이디 :** *{channel}*", inline=False)

        await ctx.send(content=f"{ctx.author.mention},", embed=setup_emb)

    @cog_ext.cog_context_menu(target=ContextMenuType.USER, name="사용자 정보 보기")
    async def ang(self, ctx: MenuContext):
        await ctx.send(f'`ID: {ctx.target_author.id}, TAG: {ctx.target_author}`')

def setup(bot):
    bot.add_cog(setupa(bot))