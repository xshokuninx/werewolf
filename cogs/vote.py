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
    
    async def night_shift(self, ctx):
        if not self.bot.game.is_set_vote():
            return
        guild = self.bot.game.channel.guild
        self.bot.game.execute()
        executed = guild.get_member(self.bot.game.executed.id)
        await self.bot.game.channel.send(f'投票の結果 {executed.display_name} さんが処刑されました')
    
    @commands.command()
    async def vote(self, ctx, arg):
        tohyosya=self.bot.game.players.get(ctx.author.id).name
        ct=0
        tflg=False
        for p in self.bot.game.players.alives:
            ct+=1
            if ct == int(arg):
                hitohyosya=p.name
                tflg=True
                self.bot.game.players.get(ctx.author.id).vote_target[self.bot.game.days] =p.id
        if tflg == True:
            if self.bot.game.votevisible == 'on':
                await self.bot.game.channel.send(f'{tohyosya}が{hitohyosya}に投票しました。')
            elif self.bot.game.votevisible == 'off':
                await self.bot.game.channel.send(f'{tohyosya}が投票しました。')
            await self.night_shift(ctx)
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
