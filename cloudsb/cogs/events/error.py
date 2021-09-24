import discord
from discord.ext import commands

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.BadArgument):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            pass
        elif isinstance(error, discord.errors.HTTPException):
            pass
        raise error

def setup(bot):
    bot.add_cog(error(bot))