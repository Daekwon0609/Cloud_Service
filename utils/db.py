import aiosqlite

async def connect_db():
    connection = await aiosqlite.connect("db/bot.db", isolation_level=None)
    cur = await connection.cursor()
    return cur