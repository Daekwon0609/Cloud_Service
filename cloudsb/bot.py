import glob
import discord
import interactions

from interactions.client import Client
from discord.ext.commands.bot import Bot

class Cloudsb(Bot):
    def __init__(self, command_prefix, **options) -> None:
        super().__init__(
            command_prefix,
            help_command=None,
            description=None,
            **options,
        )

class interactions_bot(Client):
    def __init__(self, token: str, **kwargs) -> None:
        super().__init__(
            token,
            intents=None,
            **kwargs
        )


def load_extensions(bot: Cloudsb):
    extensions = list(
        map(
            lambda path: path.replace("./", "")
            .replace(".py", "")
            .replace("\\", ".")
            .replace("/", "."),
            filter(lambda path: "__" not in path, glob.glob("./cloudsb/dpy_cogs/*/*")),
        )
    )
    
    for cog in extensions:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(e)

def load_interacntions_cogs(client: interactions_bot):
    interactions_cogs = list(
        map(
            lambda path: path.replace("./", "")
            .replace(".py", "")
            .replace("\\", ".")
            .replace("/", "."),
            filter(lambda path: "__" not in path, glob.glob("./cloudsb/inac_cogs/*/*")),
        )
    )
    
    for inac_cog in interactions_cogs:
        try:
            client.load(inac_cog)
        except Exception as e:
            print(e)


def run(token: str):
    bot = Cloudsb(command_prefix="$", intents=discord.Intents.all())
    client = interactions_bot(token=token, intent=interactions.Intents.ALL)
    load_interacntions_cogs(client)
    load_extensions(bot)
    bot.run(token, reconnect=True)
    client.start()