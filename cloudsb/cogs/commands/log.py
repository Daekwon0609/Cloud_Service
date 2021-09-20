import discord
import datetime

from discord_slash.model import ButtonStyle

from discord.ext import commands
from discord_slash.context import ComponentContext

from discord_slash import SlashContext, cog_ext

from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

from utils.db import connect_db

class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot