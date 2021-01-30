from __future__ import annotations
from typing import Optional
import random
import collections


class Player():
    """参加者
    Attributes:
        id (int): DiscordのユーザID
        role (str): 役職名
        is_dead (bool): 死亡しているか
        vote_target (Optional[Player]): 投票指定した参加者
        raid_target (Optional[Player]): 襲撃指定した参加者
        fortune_target (Optional[Player]): 占い指定した参加者
    """

    def __init__(self, discord_id: int):
        self.id = discord_id
        self.role = '村'
        self.is_dead = False
        self.vote_target = None
        self.raid_target = None
        self.fortune_target = None
        
class Players(list):
    """参加者(複数)"""
