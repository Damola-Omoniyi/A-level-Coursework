from direct.fsm.FSM import FSM
from panda3d.core import *
from direct.actor.Actor import Actor
from player import Player


class Knight(Player):
    def __init__(self, player_num, base):
        self.player_num = player_num
        self.base = base
        super().__init__(self.player_num, self.base)
        self.character = Actor("models/Knight/knight.bam",
                               {"Attack1": "models/Knight/knight_Attack1.bam",
                                "Attack2": "models/Knight/knight_Attack2.bam",
                                "Attack3": "models/Knight/knight_Attack3.bam",
                                "Attack4": "models/Knight/knight_Attack4.bam",
                                "Attack5": "models/Knight/knight_Attack5.bam",
                                "Block1": "models/Knight/knight_Block1.bam",
                                "Death1": "models/Knight/knight_Death1.bam",
                                "Death2": "models/Knight/knight_Death2.bam",
                                "Idle": "models/Knight/knight_Idle.bam",
                                "Impact1": "models/Knight/knight_Impact1.bam",
                                "Impact2": "models/Knight/knight_Impact2.bam",
                                "Intro1": "models/Knight/knight_Intro1.bam",
                                "Outro1": "models/Knight/knight_Outro1.bam",
                                "Special1": "models/Knight/knight_Special1.bam",
                                "Special2": "models/Knight/knight_Special2.bam",
                                "Special3": "models/Knight/knight_Special3.bam",
                                "Walk": "models/Knight/knight_Walk.bam",
                                "Jump": "models/Knight/knight_Jump.bam"
                                })
        self.ranges = {
            "Attack1": [437.3323516845703, 0.25],
            "Attack2": [414.7734603881836, 0.25],
            "Attack3": [471.92579650878906, 0.25],
            "Attack4": [458.37034606933594, 0.75]}
