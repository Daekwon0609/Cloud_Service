import discord
import asyncio

from datetime import datetime
from utils.db import connect_db
from utils.change import change_name
from utils.system_log import log_pr

async def check_config(bot: discord.Client):
    value_none_list = []
    cur = await connect_db()

    await cur.execute("SELECT Category, Type FROM cloud_setup")
    list_setup_value = await cur.fetchall()

    if len(list_setup_value) == 0:
        return False
    else:  
        for value in list_setup_value:
            if value[0] == 0:
                cn_value = change_name(value[1])
                value_none_list.append(cn_value)
            else:
                category = bot.get_channel(id=value[0])

                if category == None:
                    cn_value_2 = change_name(value[1])
                    value_none_list.append(cn_value_2)
        await cur.close()
        return value_none_list

async def check_channel(bot: discord.Client):
    print("충돌 확인 스크립트 시작.")
    cur = await connect_db()
    while True:
        await cur.execute("SELECT Channel FROM cloud_service")
        list_channel_value = await cur.fetchall()

        if len(list_channel_value) == 0:
            pass

        for channel_id in list_channel_value:
            true = bot.get_channel(id=channel_id[0])

            if true == None:
                await cur.execute("DELETE FROM cloud_service WHERE Channel = ?", (channel_id[0],))
                await log_pr(f"충돌 제거: ID - {channel_id[0]}")
            else:
                pass
        await asyncio.sleep(1)
        