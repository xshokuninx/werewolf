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
    async def werewolfs(self, ctx):
        if self.bot.game.players.get(ctx.author.id).role == '人狼':
            guild = self.bot.game.channel.guild
            werewolfs = ' '.join(guild.get_member(w.id).display_name for w in self.bot.game.players.werewolfs)
            await ctx.send(f'人狼 [{werewolfs}]')
            await ctx.send('あなたは人狼です')
            return
        else:
            await ctx.send('あなたは人狼ではありません')
            return
           

def setup(bot):
    return bot.add_cog(Vote(bot))
