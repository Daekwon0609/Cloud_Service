import discord

from discord_slash.utils.manage_commands import create_option, create_permission, create_choice
from discord_slash.utils.manage_components import create_button, create_actionrow

from discord_slash.model import ButtonStyle, SlashCommandPermissionType, ContextMenuType

from discord_slash import cog_ext, SlashContext
from discord_slash.context import MenuContext

from utils.db import connect_db
from utils.cn import change_name

from discord.ext import commands


class setupa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="setup",
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
                description="카테고리를 선택해주세요.",
                option_type=7,
                required=True
            )
        ],
        permissions={
            855722532107059221: [
                create_permission(
                    id=867443948585746452,
                    id_type=SlashCommandPermissionType.ROLE,
                    permission=True
                )
            ]
        }
    )
    async def add_button(self, ctx: SlashContext, categories: str, category: str):
        if str(category.type) != "category":
            return await ctx.send(hidden=True, content="카테고리 타입으로 다시 선택해주세요!")

        cur = await connect_db()

        await cur.execute("UPDATE cloud_setup SET Category = ? WHERE Type = ?", (category.id, categories))  

        categories = change_name(categories)

        setup_emb = discord.Embed(title="SETUP - COMMAND", description=f"바꾼 카테고리 종류: **[{categories}]**\n바꾼 카테고리 아이디: **{category.id}**\n\n`/setup_info` 로 전체 확인이 가능합니다.")
        
        await ctx.send(embed=setup_emb)

    @cog_ext.cog_slash(
        name="setup_info",
        description="설정된 카테고리를 보여줍니다.",
        default_permission=False,
        permissions={
            855722532107059221: [
                create_permission(
                    id=867443948585746452,
                    id_type=SlashCommandPermissionType.ROLE,
                    permission=True
                )
            ]
        }
    )
    async def setupinfo(self, ctx: SlashContext):
        setup_emb = discord.Embed(title="SETUP - INFO", description="`/setup` 으로 다시 설정할 수 있습니다.")

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

        await ctx.send(embed=setup_emb)

    @cog_ext.cog_context_menu(target=ContextMenuType.MESSAGE, name="선택")
    async def ang(self, ctx: MenuContext):
        emoji = self.bot.get_emoji(id=876463270310068315)
        button = [
            create_button(
                style=ButtonStyle.URL,
                label="바로가기",
                emoji=emoji,
                url=ctx.target_message.jump_url
            )
        ]
        row = create_actionrow(*button)
        await ctx.send(f'{ctx.target_message.author.mention}님의 **"{ctx.target_message.content}"**를 선택하셨습니다.', components=[row])


def setup(bot):
    bot.add_cog(setupa(bot))