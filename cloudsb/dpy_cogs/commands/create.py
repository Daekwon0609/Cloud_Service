import discord
import datetime

from interactions.model import ButtonStyle

from discord.ext import commands
from interactions.context import ComponentContext

from interactions import SlashContext, cog_ext

from interactions.utils.manage_commands import create_option
from interactions.utils.manage_components import create_button, create_actionrow, wait_for_component

from utils.db import connect_db
from utils.change import change_name
from utils.button_list import create_select_value, cancel_bt, scr_bt
from utils.json import load_j
from utils.system_log import log_pr

class create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="생성",
        description="문의 채널을 생성합니다.",
        guild_ids=[load_j['sub_guild']],
        options=[
            create_option(
                name="user",
                description="문의 채널을 생성할 유저의 ID를 작성해주세요.",
                option_type=3,
                required=True
            )
        ]
    )
    async def create_thred(self, ctx: SlashContext, user):
        try: user = int(user)
        except: return await ctx.send(hidden=True, content="유저의 ID를 적어주세요!")

        try: user = await self.bot.fetch_user(user_id=user)
        except: return await ctx.send(hidden=True, content=f"유저를 찾을 수 없습니다. `(사용자: {user})`")

        guild = self.bot.get_guild(id=load_j['main_guild'])
        check_member = guild.get_member(user_id=user.id)

        if check_member == None:
            return await ctx.send(hidden=True, content=f"유저를 찾을 수 없습니다. `(사용자: {user})`")
        
        cur = await connect_db()

        await cur.execute("SELECT channel FROM cloud_service where user_id = ?", (user.id,))
        null_check = await cur.fetchone()

        if null_check:
            temp_value = create_actionrow(
                create_button(
                    style=ButtonStyle.URL,
                    label="채널 바로가기",
                    url=f"https://discord.com/channels/{load_j['sub_guild']}/{null_check[0]}"
                )
            )
            return await ctx.send(hidden=True, content="이미 유저의 문의가 열려있습니다.", components=[temp_value])

        msg = await ctx.send(content=f"{ctx.author.mention},", components=[create_select_value, cancel_bt])
        try:
            select_ctx: ComponentContext = await wait_for_component(self.bot, components=[create_select_value], timeout=30)
        except TimeoutError:
            try:
                return await msg.edit(content=f"{ctx.author.mention}, `제한 시간 안에 응답하지 않아 취소하였습니다.`", components=[], embed=None)
            except discord.errors.Notfound:
                return

        await cur.execute("SELECT Category FROM cloud_setup WHERE Type = ?", (select_ctx.selected_options[0],))
        category_id = await cur.fetchone()

        category = self.bot.get_channel(id=category_id[0])

        guild_member = guild.get_member(user_id=user.id)
        guild_nickname = guild_member.display_name

        guild2 = self.bot.get_guild(id=load_j['sub_guild'])

        channel = await guild2.create_text_channel(name=f"{user.name}-{user.discriminator}", category=category)
        await cur.execute("INSERT INTO cloud_service(User_id, Channel, Message, Time, Type) VALUES(?, ?, ?, ?, ?)", (user.id, channel.id, "[관리자가 생성한 문의]", int(datetime.datetime.now().timestamp()), 2))

        len_log = None

        await cur.execute("SELECT * FROM cloud_log WHERE user_id = ?", (user.id,))
        log_check = await cur.fetchone()

        if log_check == None:
            len_log = "사용자의 첫 문의 접수입니다."
        else:
            await cur.execute("SELECT count FROM cloud_log WHERE user_id = ?", (user.id,))
            log_no = await cur.fetchone()

            len_log = f"최근 **{log_no[0]}**건의 문의 기록이 있음. 기록을 확인할려면 `/로그`를 입력하세요."
            
    
        scr_emb = discord.Embed(title=f"{user} ({user.id})", description=f"접수된 시간: <t:{int(datetime.datetime.now().timestamp())}:F>", color=discord.Colour.blurple())

        await channel.send(content="@everyone", embed=scr_emb, components=[scr_bt])
        await channel.send(content=f"닉네임: **{guild_nickname}**\n계정 생성: **<t:{int(guild_member.created_at.timestamp())}:R>**\n서버 가입: **<t:{int(guild_member.joined_at.timestamp())}:R>**\n{len_log}\n────────────────────────────────")
        
        temp_value = create_actionrow(
            create_button(
                style=ButtonStyle.URL,
                label="생성된 채널 바로가기",
                url=f"https://discord.com/channels/{load_j['sub_guild']}/{channel.id}"
            )
        )
        await select_ctx.edit_origin(content=f"{ctx.author.mention}, **{user}**님의 문의가 생성되었습니다. `(카테고리: {change_name(select_ctx.selected_options[0])})`", components=[temp_value])
        try: await user.send(f"**[시스템]:** 관리자가 문의를 임의로 생성하였습니다. `(카테고리: {change_name(select_ctx.selected_options[0])})`")
        except: pass
        finally: await log_pr(f"문의 생성(임의): {channel.name} ({channel.id})"); await channel.send(f"**[시스템]:** 관리자가 문의를 임의로 생성하였습니다. `(카테고리: {change_name(select_ctx.selected_options[0])})`")

def setup(bot):
    bot.add_cog(create(bot))

