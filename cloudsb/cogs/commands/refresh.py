from discord_slash.utils.manage_commands import remove_all_commands, create_permission
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandPermissionType
from discord.ext import commands
from utils.json import load_j

class refresh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='��ü����', 
        description="��� Slash ��ɾ �����մϴ�.", 
        guild_ids=[load_j['sub_guild']],
    )
    async def refresh(self, ctx: SlashContext):
        await remove_all_commands(self.bot.user.id, "ODY3NDM5NzEyMzM1NjkxODE2.YPhILw.yGiW3fEdNXgrg9-tFejZzky0raA", [ctx.guild.id])
        await ctx.send(hidden=True, content="��� Slash ��ɾ �����Ͽ����ϴ�.")

def setup(bot):
    bot.add_cog(refresh(bot))