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
    async def vote(self, ctx, arg):
        tohyosya=self.bot.game.players.get(ctx.author.id).name
        ct=1
        tflg=False
        for p in self.bot.game.players.alives:
            if ct == arg:
                hitohyosya=p.name
                tflg=True
        if tflg == True:
            if self.bot.game.votevisible == 'on':
                await ctx.send(f'{tohyosya}が{hitohyosya}に投票しました。')
            elif self.bot.game.votevisible == 'off':
                await ctx.send(f'{tohyosya}が 投票しました。')
        elif tflg == False:
            await ctx.send(f'{arg}はエラーです。正しく相手を選択してください')
    
    
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
