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
    
    """
    @commands.command()
    async def vote(self, ctx, arg):
        if self.bot.game.votevisible == 'on':
            await ctx.send(f'')
    """
    """
    async def tohyo(self, ctx):
        if not self.bot.game.is_set_target():
            return
    """
    @commands.command()
    async def wolflist(self, ctx):
        if self.bot.game.players.get(ctx.author.id).role != '人狼' and self.bot.game.players.get(ctx.author.id).role != '狂信者':
            await ctx.send('この村の人狼は [********] です。')
            await ctx.send('この村の狂信者は [********] です。')
            return
        werewolfs =''
        for w in self.bot.game.players.werewolfs:
            werewolfs = werewolfs + ' ' +w.name
        await ctx.send(f'この村の人狼は [{werewolfs}] です。')
        
        kyosins =''
        for k in self.bot.game.players.kyosins:
            kyosins = kyosins + ' ' +k.name
        await ctx.send(f'この村の狂信者は [{kyosins}] です。')
    
def setup(bot):
    return bot.add_cog(Vote(bot))
