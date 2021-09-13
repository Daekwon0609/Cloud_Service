import discord
import datetime

from utils.db import connect_db
from utils.change import change_name, replace_all

async def Add_log(channel: discord.TextChannel, user: discord.User, user2: discord.User, bot: discord.Client):
    LOGS = []
    badwords = {"*": "", "─": "", "`": ""}
    async for message in channel.history():
        time = message.created_at + datetime.timedelta(hours=9)
        time = f"{time.year}-{time.month}-{time.day} {time.hour}:{time.minute}:{time.second} UTC"
        if message.author == bot.user:
            if "@everyone" in message.content:
                pass
            elif message.content.startswith("닉네임:"):
                message_content = replace_all(message.content, badwords)
                LOGS.append(f"\n\n{message_content}")
            else:
                message_content = replace_all(message.content, badwords)
                LOGS.append(f"\n[{time}] {message_content}")
        else:
            time = message.created_at + datetime.timedelta(hours=9)
            time = f"{time.year}-{time.month}-{time.day} {time.hour}:{time.minute}:{time.second} UTC"

            LOGS.append(f"\n[{time}] {message.author.name}#{message.author.discriminator} : {message.content}")

    channel_time = channel.created_at + datetime.timedelta(hours=9)
    LOGS.append(f"사용자: {user.name}#{user.discriminator} ({str(user.id)}) / 시작 시간: {channel_time.year}-{channel_time.month}-{channel_time.day} {channel_time.hour}:{channel_time.minute}:{channel_time.second} UTC")
    LOGS = LOGS[::-1] # list Backwards

    cur = await connect_db()

    await cur.execute("SELECT * FROM cloud_log WHERE user_id = ?", (user.id,))
    log_check = await cur.fetchone()

    if log_check == None:
        await cur.execute("INSERT INTO cloud_log(user_id, time, count) values(?, ?, ?)", (user.id, int(datetime.datetime.now().timestamp()), 1))
    else:
        await cur.execute("UPDATE cloud_log SET count = count + ? WHERE user_id = ?", (1, user.id))

    await cur.execute("SELECT count FROM cloud_log WHERE user_id = ?", (user.id,))
    log_no = await cur.fetchone()

    log_no = log_no[0]

    file = open(f"db/log/{str(user.id)}-{str(log_no)}.txt", "w")

    for item in LOGS:
        try:
          file.write(item)
        except:
            pass

    file.close()
    file = open(f"db/log/{str(user.id)}-{str(log_no)}.txt","rb")


    await cur.execute("SELECT Category FROM cloud_setup WHERE Type = ?", ("log_channel",))
    log_channel = await cur.fetchone()

    await cur.execute("SELECT Type FROM cloud_setup WHERE Category = ?", (channel.category_id,))
    user_type = await cur.fetchone()

    user_type = change_name(user_type[0])
    log_channel = bot.get_channel(id=log_channel[0])

    await log_channel.send(content=f"**{user2}**님이 **{user}**님의 **{user_type} 타입**의 문의를 종료하였습니다.", file=discord.File(fp=file, filename="log.txt"))
