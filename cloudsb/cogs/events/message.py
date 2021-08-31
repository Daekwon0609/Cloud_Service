import discord
import datetime
from datetime import date
import os

from asyncio import TimeoutError

from discord_slash.utils.manage_components import wait_for_component

from discord_slash.context import ComponentContext

from utils.db import connect_db
from utils.change import change_name

from utils.button_list import *
from utils.json import *
from utils.sptext import *

from discord.ext import commands

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.guild:
                cur = await connect_db()

                await cur.execute("SELECT Type FROM cloud_service WHERE User_id = ?", (message.author.id,))
                service_type = await cur.fetchone()

                if service_type is None:
                    pass
                elif service_type[0] == 1:
                    return await message.channel.send("`선택하지 않은 버튼이 있습니다!`", delete_after=5)
                elif service_type[0] == 2:
                    await cur.execute("SELECT Channel FROM cloud_service WHERE User_id = ?", (message.author.id,))
                    channel = await cur.fetchone()

                    channel = self.bot.get_channel(id=channel[0])

                    if channel == None:
                        await cur.execute("DELETE FROM cloud_service WHERE User_id = ?", (message.author.id,))
                        pass

                    if len(message.attachments) != 0:
                        if len(message.content) == 0:
                            message.content = "**N/A**"
                        return await channel.send(f"**{message.author.name}:** {message.content}\n**링크:** {message.attachments[0].url}")

                    return await channel.send(f"**{message.author.name}:** {message.content}")
                
                await cur.execute("INSERT INTO cloud_service(User_id, Time, Type) VALUES(?, ?, ?)", (message.author.id, int(datetime.datetime.now().timestamp()), 1))

                msg = await message.channel.send(content="`문의할 주제를 선택해주세요.`", components=[service_buttons_1])

                try:
                    ctx: ComponentContext = await wait_for_component(self.bot, components=service_buttons_1, timeout=30)
                except TimeoutError:
                    await msg.edit(content="`제한 시간 안에 응답하지 않아 취소되었습니다!`", components=None, embed=None)
                    return await cur.execute("DELETE FROM cloud_service WHERE User_id = ?", (message.author.id,))

                await cur.execute("SELECT Category FROM cloud_setup WHERE Type = ?", (ctx.component_id,))
                category_id = await cur.fetchone()
            
                guild = self.bot.get_guild(id=load_j['main_guild'])
                category = self.bot.get_channel(id=category_id[0])

                guild_nickname = guild.get_member(user_id=message.author.id)
                guild_nickname = guild_nickname.display_name

                channel = await guild.create_text_channel(name=f"{message.author.name}-{message.author.discriminator}", category=category)
                await cur.execute(f"UPDATE cloud_service SET Channel = '{channel.id}', Type = 2, Message = '{message.content}' WHERE User_id = '{message.author.id}'")

                suf_emb = discord.Embed(title="문의가 정상적으로 접수되었습니다.", description=f"<t:{int(datetime.datetime.now().timestamp())}:F>", color=discord.Colour.green())
                suf_emb.add_field(name="문의 내용", value=message.content, inline=False)
                suf_emb.add_field(name="문의 종류", value=str(change_name(ctx.component_id)), inline=False)

                await ctx.edit_origin(content=None, embed=suf_emb, components=None)

                len_log = 1
                for file in os.listdir("db/log/"):
                    if file.startswith(f"{str(ctx.author.id)}"):
                        len_log = len_log + 1    
            
                scr_emb = discord.Embed(title=f"{ctx.author} ({ctx.author.id})", description=f"접수된 시간: <t:{int(datetime.datetime.now().timestamp())}:F>", color=discord.Colour.blurple())
                scr_emb.add_field(name="문의 내용", value=message.content, inline=False)

                await channel.send(content="@everyone", embed=scr_emb, components=[scr_bt])
                await channel.send(content=f"닉네임: **{guild_nickname}**, 뭘 해야하나 ㅋ\n최근 **{len_log}** 건의 문의 기록이 있음. 기록을 확인할려면 `/로그`를 입력하세요.\n────────────────────────────────")
            else:
                cur = await connect_db()

                await cur.execute("SELECT Channel FROM cloud_service")
                channels = await cur.fetchall()

                if len(channels) == 0:
                    await message.channel.send("Database에 등록된 채널이 없습니다.") 
                for channel in channels:
                    self_channel = self.bot.get_channel(id=channel[0])
                    if self_channel == None:
                        return await cur.execute("DELETE FROM cloud_service WHERE Channel = ?", (channel[0],))
                    if message.channel.id == self_channel.id:

                        sub_guild = self.bot.get_guild(id=load_j['sub_guild'])
                        role_name = sub_guild.get_member(user_id=message.author.id).roles

                        role_list = []
                        for role, ban_name in zip(role_name, specialtext):
                            if role.name == "@everyone":
                                continue
                            elif role.name in ban_name:
                                role_list.append(role.name)

                        if len(role_list) == 0:
                            role_list = ['N/A']

                        await cur.execute("SELECT User_id FROM cloud_service WHERE Channel = ?", (message.channel.id,))
                        user_id = await cur.fetchone()

                        main_guild = self.bot.get_guild(id=load_j['main_guild'])
                        user = main_guild.get_member(user_id=user_id[0])

                        await message.delete()

                        if len(message.attachments) != 0:
                            if len(message.content) == 0:
                                message.content = "**N/A**"
                            return await message.channel.send(f"**[{role_list[0]}]** **{message.author.name}:** {message.content}\n**링크:** {message.attachments[0].url}")
                        
                        await message.channel.send(f"**[{role_list[0]}]** **{message.author.name}:** {message.content}")
                        await user.send(f"**[{role_list[0]}]** **{message.author.name}:** {message.content}")
                    
    
def setup(bot):
    bot.add_cog(message(bot))
