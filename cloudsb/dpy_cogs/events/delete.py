from discord.ext import commands

from utils.db import connect_db
from utils.change import AM_PM

class delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):

        cur = await connect_db()

        await cur.execute("SELECT * FROM cloud_service WHERE Channel = ?", (payload.channel_id,))
        check_channel = await cur.fetchone()

        if check_channel == None:
            return

        if payload.cached_message == None:
            return
        elif payload.cached_message.content.startswith(("**[유저", "**[시스템")):
            return


        await cur.execute("SELECT User_id FROM cloud_service WHERE Channel = ?", (payload.channel_id,))
        user_data = await cur.fetchone()

        try: user = await self.bot.fetch_user(user_id=user_data[0])
        except: return

        try: dm_channel = await user.create_dm()
        except: return
        
        async for dm_msg in dm_channel.history(limit=None):
            AM_PM_value1 = dm_msg.created_at.strftime('%p')
            AM_PM_value2 = payload.cached_message.created_at.strftime('%p')
            if dm_msg.created_at.strftime(f'%Y.%m.%d. {AM_PM(AM_PM_value1)} %I:%M') == payload.cached_message.created_at.strftime(f'%Y.%m.%d. {AM_PM(AM_PM_value2)} %I:%M') and dm_msg.content == payload.cached_message.content:
                try:
                    await dm_msg.delete()
                except:
                    return
                await self.bot.get_channel(id=payload.channel_id).send(f"**[시스템]:** 메시지가 삭제되었습니다. ({dm_msg.content})")
            else:
                return

def setup(bot):
    bot.add_cog(delete(bot))

        
            
    
        
            
            