import discord
from utils.db import connect_db

async def check_config(bot: discord.Client):
    async with connect_db as cur:
        await cur.execute("SELECT Category, Type FROM cloud_setup")
        list_setup_value = await cur.fetchall()

        value = True

        if len(list_setup_value) == 0:
            return value == False
        else: 
            for value in list_setup_value:
                print(len(value[0]))
                print(value[0])

                if value[0] == 0:
                    print(value[1])
                    return value == False
        