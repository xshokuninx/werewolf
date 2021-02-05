from discord.ext import commands
from cogs.utils.player import Player

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
        name=member.mention
        player.set_name(name)
        await ctx.send(f"{member.mention}さんが参加しました。")
        self.bot.game.playct += 1

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
                self.bot.game.playct -= 1
                return await ctx.send("ゲームから退出しました。")
        return await ctx.send("ゲームに参加していません。")
    
    @commands.command()
    async def casting(self, ctx):
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        self.bot.game.casting = ''
        self.bot.game.castct =0
        
        
    @commands.command()
    async def murabito(self, ctx):
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        self.bot.game.casting = self.bot.game.casting + 'あ'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def uranaishi(self, ctx):
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        self.bot.game.casting = self.bot.game.casting + 'い'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def reibaishi(self, ctx):
        self.bot.game.casting = self.bot.game.casting + 'う'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def jinro(self, ctx):
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        self.bot.game.casting = self.bot.game.casting + 'ア'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def kyojin(self, ctx):
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        self.bot.game.casting = self.bot.game.casting + 'イ'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def kyosin(self, ctx):
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        self.bot.game.casting = self.bot.game.casting + 'ウ'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def youko(self, ctx):
        self.bot.game.casting = self.bot.game.casting + '狐'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def haitoku(self, ctx):
        if self.bot.game.status == "nothing":
            return await ctx.send("現在ゲームはありません。")
        elif self.bot.game.status == "playing":
            return await ctx.send("現在ゲーム進行中です。")
        self.bot.game.casting = self.bot.game.casting + '背'
        self.bot.game.castct += 1
        await ctx.send(f"今の配役:{self.bot.game.casting}")
        await ctx.send(f"配役人数:{self.bot.game.castct}　参加人数:{self.bot.game.playct}")
        
    @commands.command()
    async def murabitoCO(self, ctx):
        co='村人CO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
        
    @commands.command()
    async def uranaiCO(self, ctx):
        co='占いCO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
        
    @commands.command()
    async def reibaiCO(self, ctx):
        co='霊媒CO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
        
    @commands.command()
    async def jinroCO(self, ctx):
        co='人狼CO'
        player = self.bot.game.players.get(ctx.author.id).role
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
        
    @commands.command()
    async def kyojinCO(self, ctx):
        co='狂人CO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
    
    @commands.command()
    async def kyosinCO(self, ctx):
        co='狂信者CO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")

    @commands.command()
    async def yokoCO(self, ctx):
        co='妖狐CO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
        
    @commands.command()
    async def haitokuCO(self, ctx):
        co='背徳者CO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
        
    @commands.command()
    async def kakusiroCO(self, ctx):
        co='確白CO'
        player = self.bot.game.players.get(ctx.author.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
        
    @commands.command()
    async def kakukuroCO(self, ctx):
        co='確黒CO'
        member = ctx.author
        player = Player(member.id)
        player.set_co(co)
        await ctx.send(f"{player.name}さんが{player.co}しました。")
    
    @commands.command()
    async def resetb(self, ctx):
        self.role = '役無し'
        self.name = '名無し'
        self.co ='CO無し'
        self.is_dead = False
        self.vote_target = None
        self.raid_target = None
        self.fortune_target = None


def setup(bot):
    bot.add_cog(PlayersCog(bot))
