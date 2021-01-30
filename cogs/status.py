import random
from discord.ext import commands
from cogs.utils.roles import simple
from cogs.utils.errors import PermissionNotFound, NotGuildChannel


class GameStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            await self.bot.on_command_error(ctx, NotGuildChannel())
            return False

        if not ctx.author.guild_permissions.administrator:
            await self.bot.on_command_error(ctx, PermissionNotFound())
            return False

        return True
    
    
def setup(bot):
    bot.add_cog(GameStatus(bot))
