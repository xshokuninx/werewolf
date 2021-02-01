import discord
from discord.ext import commands
from cogs.utils import errors
from cogs.utils.game import Game
from cogs.utils.player import Players

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not isinstance(ctx.channel, discord.DMChannel):
            await self.bot.on_command_error(ctx, errors.NotDMChannel())
            return False
        return True
    
    @commands.command()
    async def wolflist(self, ctx):
        if self.bot.game.players.get(ctx.author.id).role != '人狼':
            await ctx.send('あなたは人狼ではありません')
            return
        werewolfs =''
        for w in self.bot.game.players.werewolfs:
            werewolfs = werewolfs + ' ' +w.role
        await ctx.send(f'この村の人狼は {werewolfs} です。')
    
def setup(bot):
    return bot.add_cog(Vote(bot))
