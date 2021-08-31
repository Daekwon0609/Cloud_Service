import discord
from utils.db import connect_db
from utils.change import change_name

async def check_config(bot: discord.Client):
    value_none_list = []
    cur = await connect_db()

    await cur.execute("SELECT Category, Type FROM cloud_setup")
    list_setup_value = await cur.fetchall()

    if list_setup_value == 0:
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
    return value_none_list
        