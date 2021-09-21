import discord
from discord.ext import commands

from utils.db import connect_db

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
        
        await cur.execute("SELECT User_id FROM cloud_service WHERE Channel = ?", (payload.channel_id,))
        user_data = await cur.fetchone()

        try: user = await self.bot.fetch_user(user_id=user_data[0])
        except: return

        dm_channel = await user.create_dm()

        await cur.execute("SELECT Last_Message FROM cloud_service WHERE Channel = ?", (payload.channel_id,))
        last = await cur.fetchone()

        async for msg in dm_channel.history():
            if msg.content == payload.cached_message.content and msg.id == last[0]:
                await msg.delete()
                await self.bot.get_channel(id=payload.channel_id).send(f"**[시스템]:** `메시지가 삭제되었습니다.` ({msg.content})")

def setup(bot):
    bot.add_cog(delete(bot))

        
            
    
        
            
            