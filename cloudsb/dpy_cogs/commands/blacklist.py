import discord
import datetime
import interactions

from utils.json import load_j
from utils.db import connect_db 
from utils.system_log import log_pr

class blacklist(interactions.Extension):
  def __init__(self, client):
    self.client: interactions.Client = client

    @client.command(
        name="블랙리스트",
        description="사용자의 블랙리스트를 관리합니다.",
        scope=[load_j['sub_guild']],
        options=[
            interactions.Option(
                name="설정",
                description="사용자의 고객센터 블랙리스트를 설정합니다.",
                type=interactions.OptionType.SUB_COMMAND,
            ),
            interactions.Option(
                name="해제",
                description="사용자의 고객센터 블랙리스트를 해제합니다.",
                type=interactions.OptionType.SUB_COMMAND,
                options=[
                    interactions.Option(
                        name="user",
                        description="블랙리스트를 해제할 사용자의 ID를 작성해주세요.",
                        type=interactions.OptionType.NUMBER,
                        required=False
                    )
                ]
            )
        ]
    )
    async def blacklist(self, ctx: interactions.CommandContext, sub_command: str, user: str):     
        cur = await connect_db()        

        if sub_command == "설정": 
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

            blacklist_emb = discord.Embed(title="블랙리스트 등록", description=f"등록 시간: <t:{int(datetime.datetime.now().timestamp())}>\n\n유저: {user.mention} (**{user.id}**)", color=discord.Colour.red())
            
            await log_pr(f"블랙리스트 등록: {user} ({user.id})")
            await ctx.send(content=f"{ctx.author.mention},", embed=blacklist_emb)
        elif sub_command == "해제":
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

                    blacklist_emb = discord.Embed(title="블랙리스트 해제", description=f"해제 시간: <t:{int(datetime.datetime.now().timestamp())}>\n\n유저: {user.mention} (**{user.id}**)", color=discord.Colour.green())
                    
                    await log_pr(f"블랙리스트 해제: {user} ({user.id})")
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

                    blacklist_emb = discord.Embed(title="블랙리스트 해제", description=f"해제 시간: <t:{int(datetime.datetime.now().timestamp())}>\n\n유저: {user.mention} (**{user.id}**)", color=discord.Colour.green())
                    
                    await log_pr(f"블랙리스트 해제: {user} ({user.id})")
                    await ctx.send(content=f"{ctx.author.mention},", embed=blacklist_emb)    

def setup(client):
    blacklist(client)