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
        village_count = 0
        werewolf_count = 0
        yokoflg = 0
        for p in self.bot.game.players.alives:
            if p.role == "人狼":
                werewolf_count += 1
            elif p.role == "妖狐":
                yokoflg = 1
            else:
                village_count += 1
        finflg=0
        if werewolf_count == 0 and yokoflg == 1:
            await self.bot.game.channel.send('人狼が全滅し、妖狐が生存しているため妖狐陣営の勝利です！')
            await self.yokowinflg(ctx)
            finflg=1
        elif werewolf_count >= village_count and yokoflg == 1:
            await self.bot.game.channel.send('人狼が村人より多く、妖狐が生存しているため妖狐陣営の勝利です！')
            await self.yokowinflg(ctx)
            finflg=1
        elif werewolf_count == 0 and village_count == 0 and yokoflg == 0:
            await self.bot.game.channel.send('全滅したため引き分けです!')
            finflg=1
        elif werewolf_count == 0:
            await self.bot.game.channel.send('人狼が全滅したため、村人陣営の勝利です！')
            await self.murawinflg(ctx)
            finflg=1
        elif werewolf_count >= village_count:
            await self.bot.game.channel.send('人狼が村人より多いため、人狼陣営の勝利です！')
            await self.jinrowinflg(ctx)
            finflg=1
        if finflg == 1:
            await self.bot.game.channel.send('<勝った人>')
            for p in self.bot.game.players.wins:
                await self.bot.game.channel.send(f'{p.name}({p.role})')
            await self.bot.game.channel.send('<負けた人>')
            for p in self.bot.game.players.s:
                await self.bot.game.channel.send(f'{p.name}({p.role})')  
            self.bot.game = Game()
    
    async def yokowinflg(self, ctx):
        for p in self.bot.game.players.alives.yokos:
            p.winflg = True
        for p in self.bot.game.players.haitokus:
            p.winflg = True
        return
    
    async def murawinflg(self, ctx):
        for p in self.bot.game.players.murabitos:
            p.winflg = True
        for p in self.bot.game.players.uranais:
            p.winflg = True
        for p in self.bot.game.players.reibais:
            p.winflg = True
        return
    
    async def jinrowinflg(self, ctx):
        for p in self.bot.game.players.werewolfs:
            p.winflg = True
        for p in self.bot.game.players.kyojins:
            p.winflg = True
        for p in self.bot.game.players.kyosins:
            p.winflg = True
        return
                
    async def noon_shift(self, ctx):
        """夜行動処理"""
        if not self.bot.game.is_set_night():
            return
        diect=[0]*(int(self.bot.game.playct)+1)
        i = 0
        
        """占い師"""
        for p in self.bot.game.players.alives.uranais:
            user = self.bot.get_user(p.id)
            hiplay=1
            for q in self.bot.game.players.alives:
                if p.night_target == q.id:                  
                    uranaisaki = q.id
                    role = q.role
                    uraname =q.name
            if role == '人狼':
                await user.send(f'{uraname}さんは人狼です')
            elif role == '妖狐':
                i+=1
                diect[i] =uranaisaki.id
                self.bot.get_user(uranaisaki).die()
                yokoflg=0
                for p in self.bot.game.players.alives.yokos:
                    yokoflg=1
                if yokoflg == 0:
                    for p in self.bot.game.players.alives.haitokus:
                        self.bot.game.players.get(p.id).die()
                        i+=1
                        diect[i] =p.name
                await user.send(f'{uraname}さんは人狼ではありません')
            else:
                await user.send(f'{uraname}さんは人狼ではありません')
        
        """人狼"""
        guild = self.bot.game.channel.guild
        tohyoct=[0]*(int(self.bot.game.playct)+1)
        for p in self.bot.game.players.alives.werewolfs:
            hiplay=1
            for q in self.bot.game.players.alives:
                if p.night_target == q.id:
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
        else:
            hiplay=1
            maxplay = random.choice(maxplay)
            for r in self.bot.game.players.alives:
                if int(maxplay) == hiplay:
                    voteid=r.id
                    votename=r.name
                hiplay+=1
        for q in self.bot.game.players.alives:
                if voteid == q.id:                  
                    role = q.role
                    """襲撃処理"""
        if maxhyo != 0 and role != '妖狐':
            self.bot.game.players.get(voteid).die()
            i+=1
            diect[i] =votename
        for ra in self.bot.game.players.alives.werewolfs:
            user = self.bot.get_user(ra.id)
            await user.send(f'人狼会議の結果{votename}を襲撃します')
            """死亡ログ処理"""
        random.shuffle(diect)
        for s in range(int(self.bot.game.playct)):
            if diect[s+1] != 0:
                await self.bot.game.channel.send(f'{diect[s+1]}さんが無残な姿で発見されました')
        for b in self.bot.game.players:
            b.night_target = None
        await self.noonck(ctx)
        await self.winflg(ctx)
    
    async def noonck(self, ctx):
        """ 朝になる前の行動"""
        self.bot.game.time = 'noon'
        self.bot.game.days += 1
        await self.bot.game.channel.send(f'{self.bot.game.days}日目 昼')
        
        
    
    async def nightck(self, ctx):
        """ 夜になる前の行動"""
        self.bot.game.time = 'night'
        await self.bot.game.channel.send(f'{self.bot.game.days}日目 夜')        
        yokoflg=0
        for nu in self.bot.game.players.alives.yokos:
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
    async def yoru(self, ctx, arg):
        if self.bot.game.time != 'night' or self.bot.game.status != 'playing':
            await ctx.send('ただいま夜時間ではないので投票できません')
            return
        if self.bot.game.players.get(ctx.author.id).is_dead == True:
            await ctx.send('あなたは死亡しているので行動できません')
            return
        if self.bot.game.players.get(ctx.author.id).is_dead == True:
            await ctx.send('あなたは行動しているので行動できません')
            return
        tohyosya=self.bot.game.players.get(ctx.author.id).name
        role = self.bot.game.players.get(ctx.author.id).role
        if role == '人狼':
            come = '襲撃先'
        elif role == '占い師':
            come = '占い先'
        else:
            come = '怪しい人'
        ct=0
        tflg=False
        for p in self.bot.game.players.alives:
            ct+=1
            if ct == int(arg):
                hitohyosya=p.name
                tflg=True
                self.bot.game.players.get(ctx.author.id).night_target = p.id
        if tflg == True:
            await ctx.send(f'{hitohyosya}を{come}として認証しました')
            await self.noon_shift(ctx)
        elif tflg == False:
            await ctx.send(f'{arg}はエラーです。正しく相手を選択してください')
        
        
    @commands.command()
    async def vote(self, ctx, arg):
        if self.bot.game.time != 'noon' or self.bot.game.status != 'playing':
            await ctx.send('ただいま投票時間ではないので投票できません')
            return
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
    async def foxlist(self, ctx):
        if self.bot.game.players.get(ctx.author.id).role != '背徳者':
            await ctx.send('この村の妖狐は [********] です。')
            return
        foxs =''
        for w in self.bot.game.players.yokos:
            foxs = foxs + ' ' +w.name
        await ctx.send(f'この村の妖狐は [{foxs}] です。')
    
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
