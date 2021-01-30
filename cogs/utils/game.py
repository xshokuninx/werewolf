from typing import Optional


class Game():
    """人狼ゲーム
    Attributes:
        status (str): 進行状況
        channel (discord.TextChannel): ゲームを進行するチャンネル
        players (Players): 参加者リスト
        days (int): ゲームの経過日
        executed (Optional[Player]): 処刑されたプレイヤー
        raided (Optional[Player]): 襲撃されたプレイヤー
        fortuned (Optional[str]): 占い結果
    """

    def __init__(self):
        self.status = 'nothing'
        self.channel = None
        self.players = Players()
        self.days = 0
        self.executed = None
        self.raided = None
        self.fortuned = None
