import discord
from discord.ext import commands
from cogs.utils import errors
from cogs.utils.game import Game
from cogs.utils.player import Players
from cogs.utils.pagenator import Pagenator


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    return bot.add_cog(Vote(bot))
