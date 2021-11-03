from discord.ext import commands

from utils.db import connect_db
class left(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cur = await connect_db()

        await cur.execute("SELECT Channel FROM cloud_service WHERE User_id = ?", (member.id,))
        check_channel = await cur.fetchone()

        if check_channel == None:
            return
        try:
            del_msg = await self.bot.get_channel(id=check_channel[0]).send("@everyone")

        except:
            pass
        else:
            await del_msg.delete()
            await self.bot.get_channel(id=check_channel[0]).send(f"**[시스템]:** 문의 진행 중에 사용자가 서버를 나갔습니다. ({member.mention})")

        await cur.execute("SELECT Category FROM cloud_setup WHERE Type = ?", ("log_channel",))
        log_channel = await cur.fetchone()

        log_channel = self.bot.get_channel(id=log_channel[0])

        await log_channel.send(f"{member} ({member.id}) 님이 나갔습니다. (유저와 관련된 채널을 삭제해주세요.)")
        
        await cur.execute("UPDATE cloud_service SET Type = ? WHERE User_id = ?", (3, member.id))

def setup(bot):
    bot.add_cog(left(bot))