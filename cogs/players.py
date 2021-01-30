from discord.ext import commands
from cogs.utils.player import Player
from cogs.utils.game import Game


class PlayersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """ゲームに参加するコマンド"""
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        member = ctx.author
        for p in self.bot.game.players:
            if member.id == p.id:
                return await ctx.send("すでにゲームに参加しています。")
        player = Player(member.id)
        self.bot.game.players.append(player)
        await ctx.send(f"{member.mention}さんが参加しました。")

    @commands.command()
    async def leave(self, ctx):
        """ゲームから退出するコマンド"""
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("既にゲームが始まっているため退出できません。")
        member = ctx.author
        for p in self.bot.game.players:
            if member.id == p.id:
                self.bot.game.players.remove(p)
                return await ctx.send("ゲームから退出しました。")
        return await ctx.send("ゲームに参加していません。")
    
    @commands.command()
    async def casting(self, ctx):
        self.bot.game.casting = ''
        self.bot.game.castct =0
        
        
    @commands.command()
    async def murabito(self, ctx):
        self.bot.game.casting = self.bot.game.casting + 'あ'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        wait ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def uranaishi(self, ctx):
        self.bot.game.casting = self.bot.game.casting + 'い'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        wait ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def reibaishi(self, ctx):
        self.bot.game.casting = self.bot.game.casting + 'う'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        wait ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def jinro(self, ctx):
        self.bot.game.casting = self.bot.game.casting + 'ア'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        wait ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def youko(self, ctx):
        self.bot.game.casting = self.bot.game.casting + '狐'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        wait ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")


def setup(bot):
    bot.add_cog(PlayersCog(bot))
