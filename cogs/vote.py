import random
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
    
    async def winflg(self, ctx):
        await self.bot.game.channel.send('勝利判定')
        village_count = 0
        werewolf_count = 0
        yokoflg = 0
        for p in self.players.alives:
            if p.role == "人狼":
                werewolf_count += 1
            elif p.role == "妖狐":
                yokoflg = 1
            else:
                village_count += 1
                
        if werewolf_count == 0 and yokoflg == 1:
            await self.bot.game.channel.send('人狼が全滅し、妖狐が生存しているため妖狐陣営の勝利です！')
            return
        elif werewolf_count >= village_count and yokoflg == 1:
            await self.bot.game.channel.send('人狼が村人より多く、妖狐が生存しているため妖狐陣営の勝利です！')
            return
        elif werewolf_count == 0:
            await self.bot.game.channel.send('人狼が全滅したため、村人陣営の勝利です！')
            return
        elif werewolf_count >= village_count:
            await self.bot.game.channel.send('人狼が村人より多いため、人狼陣営の勝利です！')
            return
            
        
    async def nightck(self, ctx):
        """ 夜になる前の行動"""
        self.bot.game.time = 'night'
        await self.bot.game.channel.send(f'{self.bot.game.days}日目 夜')
        
        yokoflg=0
        for p in self.bot.game.players.alives.yokos:
            yokoflg=1
        if yokoflg == 0:
            for p in self.bot.game.players.alives.haitokus:
                self.bot.game.players.get(p.id).die()
                await self.bot.game.channel.send(f'{p.name}が後追い自殺しました')
           
        
    async def night_shift(self, ctx):
        """投票処理"""
        if not self.bot.game.is_set_vote():
            return
        guild = self.bot.game.channel.guild
        """ 投票先判定 """
        tohyoct=[0]*(int(self.bot.game.playct)+1)
        for p in self.bot.game.players.alives:
            hiplay=1
            for q in self.bot.game.players.alives:
                if p.vote_target == q.id:
                    tohyoct[hiplay]+=1
                hiplay+=1
        maxhyo=0
        maxplay=''
        for num in range(self.bot.game.playct):
            nums=num+1
            if maxhyo < tohyoct[nums]:
                maxhyo = tohyoct[nums]
                maxplay=str(nums)
            elif maxhyo == tohyoct[nums]:
                maxplay = maxplay + str(nums)
        if len(maxplay) == 1:
            hiplay=1
            for r in self.bot.game.players.alives:
                if int(maxplay) == hiplay:
                    voteid=r.id
                    votename=r.name
                hiplay+=1
            await self.bot.game.channel.send(f'投票の結果 最多票の{votename}さんが処刑されました')
        else:
            hiplay=1
            maxplay = random.choice(maxplay)
            for r in self.bot.game.players.alives:
                if int(maxplay) == hiplay:
                    voteid=r.id
                    votename=r.name
                hiplay+=1
            await self.bot.game.channel.send(f'投票の結果 最多票の中から抽選で{votename}さんが処刑されました')
        self.bot.game.players.get(voteid).die()
        """投票初期化"""
        for b in self.bot.game.players:
            b.vote_target = None
        """勝敗 各プレイヤーへの送信"""
        await self.nightck(ctx)
        reilog='人狼ではありません'
        if self.bot.game.players.get(voteid).role == '人狼':
            reilog='人狼です'
        for p in self.bot.game.players.alives.reibais:
            user = self.bot.get_user(p.id)
            await user.send(f'{votename}さんは{reirog}')
        await self.winflg(ctx)
    
    @commands.command()
    async def vote(self, ctx, arg):
        if self.bot.game.players.get(ctx.author.id).is_dead == True:
            await ctx.send('あなたは死亡しているので投票できません')
            return
        tohyosya=self.bot.game.players.get(ctx.author.id).name
        ct=0
        tflg=False
        for p in self.bot.game.players.alives:
            ct+=1
            if ct == int(arg):
                hitohyosya=p.name
                tflg=True
                self.bot.game.players.get(ctx.author.id).vote_target = p.id
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
        
    @commands.command()
    async def j(self, ctx, arg):
        if self.bot.game.players.get(ctx.author.id).role != '人狼' and self.bot.game.players.get(ctx.author.id).role != '狂信者':
            await ctx.send('あなたは狼語を話せません。')
            return
        sendname = self.bot.game.players.get(ctx.author.id).name
        await self.bot.game.channel.send('アオォォォォォォン')
        for w in self.bot.game.players.werewolfs:
            user = self.bot.get_user(w.id)
            await user.send(f'({sendname}){arg}')
        for p in self.bot.game.players.kyosins:
            user = self.bot.get_user(p.id)
            await user.send(f'({sendname}){arg}')
        
    
def setup(bot):
    return bot.add_cog(Vote(bot))
