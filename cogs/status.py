import random
from discord.ext import commands
from cogs.utils.game import Game
from cogs.utils.player import Players
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

    @commands.command()
    async def create(self, ctx):
        """ゲームを作成するコマンド"""
        if self.bot.game.status == 'playing':
            await ctx.send('ゲーム中です')
            return
        if self.bot.game.status == 'waiting':
            await ctx.send('既に参加者募集中です')
            return
        self.bot.game.status = 'waiting'
        self.bot.game.channel = ctx.channel
        await ctx.send('参加者の募集を開始しました')

    @commands.command()
    async def start(self, ctx):
        """ゲームを開始するコマンド"""
        if self.bot.game is None:
            await ctx.send('まだ参加者を募集していません')
            return
        if self.bot.game.status == 'playing':
            await ctx.send('既にゲーム中です')
            return
        
        if not self.bot.game.castct == self.bot.game.playct:
            await ctx.send('配役人数と参加人数が一致していません')
            await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
            return            
        
        n = len(self.bot.game.players)
        role = self.bot.game.casting
        role_list = random.sample(role, n)
        for i in range(n):
            player = self.bot.game.players[i]
            user = self.bot.get_user(player.id)
            ranpas =role_list[i]
            if ranpas  =='あ':
                role='村人'
            elif ranpas  =='い':
                role='占い師'
            elif ranpas  =='う':
                role='霊媒師'
            elif ranpas =='ア':
                role='人狼'
            elif ranpas =='イ':
                role='狂人'
            elif ranpas =='ウ':
                role='狂信者'
            elif ranpas =='狐':
                role='妖狐'
            elif ranpas =='背':
                role='背徳者'
            player.set_role(role)
            await user.send(f'あなたの役職は{role}です')
            

        await ctx.send('-0日目夜-')
        self.bot.game.status = 'playing'
        await ctx.send('ＧＭから配布された役職を確認し、翌日に備えてください.')
    
    @commands.command()
    async def playerlist(self, ctx):
        if self.bot.game.time == 'noon':
            await ctx.send('投票先は/voteに指定したい名前のまえにあるアルファベットをつけて入力してください(/vote 1 など)')
        elif self.bot.game.time == 'night':
            await ctx.send('夜行動は/nightに指定したい名前のまえにあるアルファベットをつけて入力してください(/night 1 など)')
        ct=1
        for p in self.bot.game.players.alives:
            await ctx.send(f'{ct} {p.name}({p.co})')
            ct+=1
        
    
    @commands.command()
    async def reset(self, ctx):
        self.bot.game.casting =''
        self.bot.game.castct = 0
        self.bot.game.status = 'nothing'
        self.bot.game.channel = None
        self.bot.game.players = Players()
        self.bot.game.playct = 0
        self.bot.game.days = 0
        self.bot.game.time = 'night'
        self.bot.game.executed = None
        self.bot.game.raided = None
        self.bot.game.fortuned = None
    
    """仮設定"""
    @commands.command()
    async def tskip(self, ctx):
        if self.bot.game.time == 'noon':
            self.bot.game.time = 'night'
            await ctx.send(f'{self.bot.game.days}日目 夜')
        elif self.bot.game.time == 'night':
            self.bot.game.time = 'noon'
            self.bot.game.days += 1
            await ctx.send(f'{self.bot.game.days}日目 昼')
            
        
def setup(bot):
    bot.add_cog(GameStatus(bot))
