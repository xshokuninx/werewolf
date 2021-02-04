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
        self.role = '役無し'
        self.name = '名無し'
        self.co = 'CO無し'
        self.is_dead = False
        self.vote_target = None
        self.raid_target = None
        self.fortune_target = None
    
    def die(self):
        """死亡する"""
        self.is_dead = True
        return self
    
    def set_role(self, role: str):
        self.role = role
        return self
    
    def set_co(self, co: str):
        self.co = co
        return self
    
    def set_name(self, name: str):
        self.name = name
        return self
        
class Players(list):
    """参加者(複数)"""
    
    @property
    def memid(self) -> Players:
        """ID"""
        return Players(p.id for p in self )
    
    @property
    def alives(self) -> Players:
        """生存者(複数)"""
        return Players(p for p in self if not p.is_dead)

    @property
    def werewolfs(self) -> Players:
        """人狼(複数)"""
        return Players(p for p in self if p.role == '人狼')
    
    @property
    def kyosins(self) -> Players:
        """狂信者(複数)"""
        return Players(p for p in self if p.role == '狂信者')
    
    @property
    def most(self) -> Player:
        """最頻参加者"""
        return Player
    
    def get(self, player_id) -> Player:
        for p in self:
            if p.id == player_id:
                return p
