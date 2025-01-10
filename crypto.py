from direct.fsm.FSM import FSM
from panda3d.core import *
from direct.actor.Actor import Actor
from player import Player


class Crypto(Player):
    def __init__(self, player_num, base):
        self.player_num = player_num
        self.base = base
        super().__init__(self.player_num, self.base)

        self.character = Actor("models/Crypto/Crypto.bam",
                            {"Attack1": "models/Crypto/Crypto_Attack1.bam",
                             "Attack2": "models/Crypto/Crypto_Attack2.bam",
                             "Attack6": "models/Crypto/Crypto_Attack3.bam",
                             "Attack5": "models/Crypto/Crypto_Attack4.bam",
                             "Attack4": "models/Crypto/Crypto_Attack5.bam",
                             "Attack3-p": "models/Crypto/Crypto_Attack6.bam",
                             "Block1": "models/Crypto/Crypto_Block1.bam",
                             "Death1": "models/Crypto/Crypto_Death1.bam",
                             "Idle": "models/Crypto/Crypto_Idle.bam",
                             "Impact1": "models/Crypto/Crypto_Impact1.bam",
                             "Intro1": "models/Crypto/Crypto_Intro1.bam",
                             "Outro1": "models/Crypto/Crypto_Outro1.bam",
                             "Special1": "models/Crypto/Crypto_Special1.bam",
                             "Special2": "models/Crypto/Crypto_Special2.bam",
                             "Attack3": "models/Crypto/Crypto_Special3.bam",
                             "Special1": "models/Crypto/Crypto_Special4.bam",
                             "Special2": "models/Crypto/Crypto_Special5.bam",
                             "Walk": "models/Crypto/Crypto_Walk.bam",
                             "Jump": "models/Crypto/Crypto_Jump.bam"
                             })

        self.ranges = {
            "Attack1": [358.362060546875, 0.25],
            "Attack2": [433.4682922363281, 0.25],
            "Attack3": [358.3881530761719, 0.5],
            "Attack4": [282.9663848876953, 0.25]}


