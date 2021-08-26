import discord
import os
import datetime

from utils.db import connect_db
from utils.change import change_name

async def Add_log(channel: discord.TextChannel, user: discord.User, user2: discord.User, bot: discord.Client):
    LOGS = []
    async for message in channel.history():
        if message.author == bot.user:
            if "@everyone" in message.content:
                pass
            else:
                time = message.created_at + datetime.timedelta(hours=9)
                time = f"{time.year}-{time.month}-{time.day} {time.hour}:{time.minute}:{time.second} UTC"
                message_content = message.content.replace("*", "")
                LOGS.append(f"\n[{time}] {message_content}")
        else:
            time = message.created_at + datetime.timedelta(hours=9)
            time = f"{time.year}-{time.month}-{time.day} {time.hour}:{time.minute}:{time.second} UTC"

            LOGS.append(f"\n[{time}] {message.author.name}#{message.author.discriminator} : {message.content}")

    channel_time = channel.created_at + datetime.timedelta(hours=9)
    LOGS.append(f"사용자: {user.name}#{user.discriminator} ({str(user.id)}) / 문의 시간: {channel_time.year}-{channel_time.month}-{channel_time.day} {channel_time.hour}:{channel_time.minute}:{channel_time.second} UTC")
    LOGS = LOGS[::-1]

    log_no = 1
    for file in os.listdir("db/log/"):
       if file.startswith(f"{str(user.id)}"):
           log_no = log_no + 1

    file = open(f"db/log/{str(user.id)}-{str(log_no)}.txt", "w")

    print(LOGS)

    for item in LOGS:
        try:
          file.write(item)
        except:
            pass

    print(file)

    file.close()
    file = open(f"db/log/{str(user.id)}-{str(log_no)}.txt","rb")

    cur = await connect_db()

    await cur.execute("SELECT Category FROM cloud_setup WHERE Type = ?", ("log_channel",))
    log_channel = await cur.fetchone()

    await cur.execute("SELECT Type FROM cloud_setup WHERE Category = ?", (channel.category_id,))
    user_type = await cur.fetchone()

    user_type = change_name(user_type[0])
    log_channel = bot.get_channel(id=log_channel[0])

    await log_channel.send(content=f"**{user2}**님이 **{user}**님의 **{user_type} 타입**의 문의를 종료하였습니다.", file=discord.File(fp=file, filename="log.txt"))
