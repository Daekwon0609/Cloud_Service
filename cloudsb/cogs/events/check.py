import discord
from utils.db import connect_db

async def check_config(bot: discord.Client):
    async with connect_db as cur:
        await cur.execute("SELECT Category FROM cloud_setup")
        list_setup_value = await cur.fetchall()

        for value in list_setup_value:
            