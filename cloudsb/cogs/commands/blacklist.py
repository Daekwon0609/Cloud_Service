import discord
import datetime

from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashContext, cog_ext

from utils.json import load_j
from utils.db import connect_db 

from discord.ext import commands

class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="블랙리스트",
        name="설정",
        description="사용자의 고객센터 블랙리스트를 설정합니다.",
        guild_ids=[load_j['sub_guild']]
    )
    async def blacklist(self, ctx: SlashContext):        
        cur = await connect_db()     

        await cur.execute("SELECT Channel FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
        channel = await cur.fetchone()

        if channel == None or ctx.channel.id != channel[0]:
            return await ctx.send(content=f"{ctx.author.mention}, `해당 채널은 문의 채널이 아닙니다!`")

        await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
        user_id = await cur.fetchone()

        try: user = await self.bot.fetch_user(user_id=user_id[0])
        except: return await ctx.send(hidden=True, content=f"유저를 찾을 수 없습니다. `(사용자: {user_id[0]})`")
        
        if user == None: 
            return await ctx.send(f"유저를 찾을 수 없습니다. `(사용자: {user})`")
        
        await cur.execute("SELECT user_id FROM cloud_blacklist WHERE user_id = ?", (user.id,))
        user_same = await cur.fetchone()

        if user_same == None:
            pass
        elif user_same[0] == user.id:
            return await ctx.send(hidden=True, content=f"이미 블랙리스트 유저이므로 취소되었습니다. `(유저 아이디: {user.id})`")
        
        await cur.execute("INSERT INTO cloud_blacklist(user_id, time) values(?, ?)", (user.id, int(datetime.datetime.now().timestamp())))

        blacklist_emb = discord.Embed(title="BLACKLIST - COMMAND", description=f"등록 시간: <t:{int(datetime.datetime.now().timestamp())}>\n\n유저: {user.mention} (**{user.id}**)", color=discord.Colour.red())
        
        await ctx.send(content=f"{ctx.author.mention},", embed=blacklist_emb)

    @cog_ext.cog_subcommand(
        base="블랙리스트",
        name="해제",
        description="사용자의 고객센터 블랙리스트를 해제합니다.",
        guild_ids=[load_j['sub_guild']],
        options=[
            create_option(
                name="user",
                description="문의 채널을 생성할 유저의 ID를 작성해주세요.",
                option_type=3,
                required=False
            )
        ]
    )
    async def blacklist_disable(self, ctx: SlashContext, user = None):
        if user == None:
            cur = await connect_db()     

            await cur.execute("SELECT Channel FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
            channel = await cur.fetchone()

            if channel == None or ctx.channel.id != channel[0]:
                return await ctx.send(content=f"{ctx.author.mention}, `해당 채널은 문의 채널이 아닙니다! ID를 추가로 작성하거나 채널을 다시 확인해주세요!`")

            await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
            user_id = await cur.fetchone()

            try: user = await self.bot.fetch_user(user_id=user_id[0])
            except: return await ctx.send(hidden=True, content=f"유저를 찾을 수 없습니다. `(사용자: {user_id[0]})`")
            
            if user == None: 
                return await ctx.send(f"유저를 찾을 수 없습니다. `(사용자: {user})`")

            await cur.execute("SELECT user_id FROM cloud_blacklist WHERE User_id = ?", (user.id,))
            user_same = await cur.fetchone()

            if user_same == None:
                return await ctx.send(hidden=True, content=f"블랙리스트 유저가 아니므로 취소되었습니다. `(유저 아이디: {user.id})`")
            elif user_same[0] == user.id:
                await cur.execute("DELETE FROM cloud_blacklist WHERE User_id = ?", (user.id,))

                blacklist_emb = discord.Embed(title="BLACKLIST DISABLE - COMMAND", description=f"해제 시간: <t:{int(datetime.datetime.now().timestamp())}>\n\n유저: {user.mention} (**{user.id}**)", color=discord.Colour.green())
                
                return await ctx.send(content=f"{ctx.author.mention},", embed=blacklist_emb)
        else:
        
            try: user = int(user)
            except: return await ctx.send(hidden=True, content="유저의 ID를 적어주세요!")

            try: user = await self.bot.fetch_user(user_id=user)
            except: return await ctx.send(hidden=True, content=f"유저를 찾을 수 없습니다. `(사용자: {user})`")

            guild = self.bot.get_guild(id=load_j['main_guild'])
            check_member = guild.get_member(user_id=user.id)

            if check_member == None:
                return await ctx.send(hidden=True, content=f"유저를 찾을 수 없습니다. `(사용자: {user})`")
            
            cur = await connect_db()

            await cur.execute("SELECT user_id FROM cloud_blacklist WHERE User_id = ?", (user.id,))
            user_same = await cur.fetchone()

            if user_same == None:
                return await ctx.send(hidden=True, content=f"블랙리스트 유저가 아니므로 취소되었습니다. `(유저 아이디: {user.id})`")
            elif user_same[0] == user.id:
                await cur.execute("DELETE FROM cloud_blacklist WHERE User_id = ?", (user.id,))

                blacklist_emb = discord.Embed(title="BLACKLIST DISABLE - COMMAND", description=f"해제 시간: <t:{int(datetime.datetime.now().timestamp())}>\n\n유저: {user.mention} (**{user.id}**)", color=discord.Colour.green())
                
                await ctx.send(content=f"{ctx.author.mention},", embed=blacklist_emb)



    

def setup(bot):
    bot.add_cog(blacklist(bot))