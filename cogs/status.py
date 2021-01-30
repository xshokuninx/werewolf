import random
from discord.ext import commands
from cogs.utils.game import Game
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
            elseif ranpas  =='い':
                role='占い師'
            elseif ranpas  =='う':
                role='霊媒師'
            elseif ranpas =='ア':
                role='人狼'
            elseif ranpas =='狐':
                role='妖狐'
              
            await user.send(f'あなたの役職は{role}です')
            self.role =role

        await ctx.send('-0日目夜-')
        self.bot.game.status = 'playing'
        await ctx.send('ＧＭから配布された役職を確認し、翌日に備えてください.')
        
def setup(bot):
    bot.add_cog(GameStatus(bot))
