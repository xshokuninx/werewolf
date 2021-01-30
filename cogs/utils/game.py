from typing import Optional
from cogs.utils.player import Player, Players


class Game():
    """人狼ゲーム
    Attributes:
        casting (str):簡易版配役
        status (str): 進行状況
        channel (discord.TextChannel): ゲームを進行するチャンネル
        players (Players): 参加者リスト
        days (int): ゲームの経過日
        time (str):ゲームの時間（night:夜行動 noon:投票)
        executed (Optional[Player]): 処刑されたプレイヤー
        raided (Optional[Player]): 襲撃されたプレイヤー
        fortuned (Optional[str]): 占いされたプレイヤー
    """

    def __init__(self):
        self.casting =''
        self.status = 'nothing'
        self.channel = None
        self.players = Players()
        self.days = 0
        self.time = 'night'
        self.executed = None
        self.raided = None
        self.fortuned = None
        
