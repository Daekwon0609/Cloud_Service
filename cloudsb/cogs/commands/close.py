import asyncio

from discord_slash import cog_ext, SlashContext

from utils.json import load_j
from utils.db import connect_db
from utils.logging import Add_log
from utils.system_log import log_pr

from discord.ext import commands

class close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='종료',
        description="진행 중인 문의를 종료합니다.",
        guild_ids=[load_j['sub_guild']]
    )
    async def close(self, ctx: SlashContext):
        cur = await connect_db()

        await cur.execute("SELECT Channel FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
        channel = await cur.fetchone()

        await cur.execute("SELECT Type FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
        service_type = await cur.fetchone()

        if channel == None or ctx.channel.id != channel[0]:
            return await ctx.send(content=f"{ctx.author.mention}, `해당 채널은 문의 채널이 아닙니다!`")
        elif service_type[0] == 3:
            await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
            user_id = await cur.fetchone()

            user = self.bot.get_user(id=user_id[0])

            await ctx.send(f"{ctx.author.mention}, 문의가 5초 뒤에 종료됩니다.")

            await asyncio.sleep(5)

            await Add_log(ctx.channel, user, ctx.author, self.bot, False)
            await cur.execute("DELETE FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
            await log_pr(f"문의 종료: {ctx.channel.name} ({ctx.channel.id}))")

            return await ctx.channel.delete()
        else:
            await cur.execute("SELECT User_id FROM cloud_service WHERE Channel= ?", (ctx.channel.id,))
            user_id = await cur.fetchone()

            user = self.bot.get_user(id=user_id[0])

            await ctx.send(f"{ctx.author.mention}, 문의가 5초 뒤에 종료됩니다.")

            await asyncio.sleep(5)

            await Add_log(ctx.channel, user, ctx.author, self.bot, True)
            await cur.execute("DELETE FROM cloud_service WHERE Channel = ?", (ctx.channel.id,))
            await log_pr(f"문의 종료: {ctx.channel.name} ({ctx.channel.id})")
            await ctx.channel.delete()
            
            await user.send("`문의가 종료되었습니다.`")

def setup(bot):
    bot.add_cog(close(bot))