import discord
import datetime
import asyncio

from asyncio import TimeoutError

from discord_slash.utils.manage_components import wait_for_component

from discord_slash.context import ComponentContext
from discord_slash import cog_ext, SlashContext

from utils.db import connect_db
from utils.cn import change_name

from utils.bt import *

from discord.ext import commands

class move(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="move",
        options=[
            
        ]
    )