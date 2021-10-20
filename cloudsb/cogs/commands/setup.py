import discord

from discord_slash.utils.manage_commands import create_option, create_permission, create_choice

from discord_slash.model import SlashCommandPermissionType

from discord_slash import cog_ext, SlashContext

from utils.db import connect_db
from utils.change import change_name, change_type
from utils.json import load_j

from discord.ext import commands


class setupa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="설정",
        description="고객센터 시스템을 설정합니다.",
        default_permission=False,
        guild_ids=[load_j['sub_guild']],
        options=[
            create_option(
                name="categories",
                description="설정할 카테고리의 종류를 선택해주세요. (로그채널은 별도 설정입니다.)",
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
                    ),
                    create_choice(
                        name="로그채널",
                        value="log_channel"
                    )
                ]
            ),
            create_option(
                name="category",
                description="설정할 카테고리의 이름을 작성하거나, 선택해주세요. (ex. 카테고리 이름)",
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
        cur = await connect_db()

        if str(category.type) != "category":
            if str(categories) == "log_channel":
                if str(category.type) != "text":
                    return await ctx.send(hidden=True, content="`[텍스트]` 타입으로 다시 선택해주세요")
            else:
                return await ctx.send(hidden=True, content="`[카테고리]` 타입으로 다시 선택해주세요!")

        category = self.bot.get_channel(id=category.id)

        await cur.execute("SELECT Category FROM cloud_setup WHERE Category = ? and Type = ?", (category.id, categories))
        same_id = await cur.fetchone()

        if same_id == None:
            pass
        elif same_id[0] == category.id:
            categories = change_name(categories)
            return await ctx.send(hidden=True, content=f"중복된 내용이므로 취소되었습니다. `(종류: {categories}, 아이디: {category.id})`")

        await cur.execute("UPDATE cloud_setup SET Category = ? WHERE Type = ?", (category.id, categories))

        categories = change_name(categories)

        setup_emb = discord.Embed(title="기본 설정", description=f"`/정보` 로 전체 확인이 가능합니다.\n\n바꾼 카테고리 종류: **[{categories}]**\n바꾼 아이디: **{category.id}**")
        
        await ctx.send(content=f"{ctx.author.mention},", embed=setup_emb)

    @cog_ext.cog_slash(
        name="정보",
        description="고객센터 봇의 설정된 정보를 볼 수 있습니다.",
        default_permission=False,
        guild_ids=[load_j['sub_guild']],
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
        setup_emb = discord.Embed(title="설정 정보", description="`/설정` 으로 다시 설정할 수 있습니다.")
        cur = await connect_db()
                
        await cur.execute("SELECT Category, Type FROM cloud_setup")
        list_categ = await cur.fetchall()

        for categ in list_categ:
            type = change_name(categ[1])
            type_2 = change_type(categ[1])
            id = self.bot.get_channel(id=categ[0])

            try:
                channel = id.id
            except AttributeError:
                setup_emb.add_field(name=f"종류: [{type}] - ({type_2}) ", value=f"**아이디 :** *N/A*", inline=False)
            else:
                if type_2 == "채널":
                    setup_emb.add_field(name=f"종류: [{type}] - ({type_2})", value=f"**아이디 :** *{channel}* - {id.mention}", inline=False)
                else:
                    setup_emb.add_field(name=f"종류: [{type}] - ({type_2})", value=f"**아이디 :** *{channel}*", inline=False)

        await ctx.send(content=f"{ctx.author.mention},", embed=setup_emb)

def setup(bot):
    bot.add_cog(setupa(bot))