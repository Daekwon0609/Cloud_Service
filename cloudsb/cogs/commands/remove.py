from discord_slash.utils.manage_commands import remove_all_commands, create_permission
from discord_slash import cog_ext, SlashContext
from discord_slash.model import ButtonStyle, SlashCommandPermissionType
from discord.ext import commands

class remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='refresh', 
        description="모든 Slash 명령어를 삭제합니다.", 
        default_permission=False,
        permissions={
            855722532107059221: [
                create_permission(
                    id=720112607268307004,
                    id_type=SlashCommandPermissionType.USER,
                    permission=True
                )
            ]
        }
    )
    async def refresh(self, ctx: SlashContext):
        await remove_all_commands(self.bot.user.id, "ODY3NDM5NzEyMzM1NjkxODE2.YPhILw.yGiW3fEdNXgrg9-tFejZzky0raA", [ctx.guild.id])
        await ctx.send(hidden=True, content="모든 Slash 명령어를 삭제하였습니다.")

def setup(bot):
    bot.add_cog(remove(bot))