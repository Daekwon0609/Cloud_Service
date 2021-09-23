import glob
import discord

from discord_slash import SlashCommand
from discord.ext.commands.bot import Bot

class Cloudsb(Bot):
    def __init__(self, command_prefix, **options) -> None:
        super().__init__(
            command_prefix,
            help_command=None,
            description=None,
            **options,
        )

def load_extensions(bot: Cloudsb):
    extensions = list(
        map(
            lambda path: path.replace("./", "")
            .replace(".py", "")
            .replace("\\", ".")
            .replace("/", "."),
            filter(lambda path: "__" not in path, glob.glob("./cloudsb/cogs/*/*")),
        )
    )
    
    for cog in extensions:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(e)


def run(token: str):
    bot = Cloudsb(command_prefix="v", intents=discord.Intents.all())
    SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
    load_extensions(bot)
    bot.run(token)