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
        raid_target (Optional[Player]): 襲撃指定した参加者(使わない)
        fortune_target (Optional[Player]): 占い指定した参加者(使わない)
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
        self.yoru_target =None
        self.winflg = False
    
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
    def wins(self) -> Players:
        """勝利者(複数)"""
        return Players(p for p in self if p.winflg == True)
    
    @property
    def loses(self) -> Players:
        """敗北者(複数)"""
        return Players(p for p in self if p.winflg == False)
   
    @property
    def murabitos(self) -> Players:
        """村人(複数)"""
        return Players(p for p in self if p.role == '村人')
   
    @property
    def panyas(self) -> Players:
        """パン屋(複数)"""
        return Players(p for p in self if p.role == 'パン屋')
    
    @property
    def uranais(self) -> Players:
        """占い師(複数)"""
        return Players(p for p in self if p.role == '占い師')
    
    @property
    def reibais(self) -> Players:
        """霊媒師(複数)"""
        return Players(p for p in self if p.role == '霊媒師')
    
    @property
    def kariudos(self) -> Players:
        """狩人(複数)"""
        return Players(p for p in self if p.role == '狩人')
    
    @property
    def werewolfs(self) -> Players:
        """人狼(複数)"""
        return Players(p for p in self if p.role == '人狼')
    
    @property
    def kyojins(self) -> Players:
        """狂人(複数)"""
        return Players(p for p in self if p.role == '狂人')
    
    @property
    def kyosins(self) -> Players:
        """狂信者(複数)"""
        return Players(p for p in self if p.role == '狂信者')
  
    @property
    def yokos(self) -> Players:
        """妖狐(複数)"""
        return Players(p for p in self if p.role == '妖狐')
    
    @property
    def haitokus(self) -> Players:
        """背徳者(複数)"""
        return Players(p for p in self if p.role == '背徳者')
    
    def get(self, player_id) -> Player:
        for p in self:
            if p.id == player_id:
                return p
