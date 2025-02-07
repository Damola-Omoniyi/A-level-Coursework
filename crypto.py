from direct.fsm.FSM import FSM
from panda3d.core import *
from direct.actor.Actor import Actor
from player import Player
import complexpbr


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
                             "Special3": "models/Crypto/Crypto_Special4.bam",
                             "Special4": "models/Crypto/Crypto_Special5.bam",
                             "Walk": "models/Crypto/Crypto_Walk.bam",
                             "Jump": "models/Crypto/Crypto_Jump.bam"
                             })

        self.ranges = {
            "Attack1": [358.362060546875, 0.25],
            "Attack2": [433.4682922363281, 0.25],
            "Attack3": [358.3881530761719, 0.5],
            "Attack4": [282.9663848876953, 0.25]}

        self.atk_sound = self.base.loader.loadSfx("models/qubodupPunch01.ogg")

    def set_light(self):
        d_light = DirectionalLight('d_light')
        a_light = AmbientLight('a_light')
        d_light_np = self.character.attachNewNode(d_light)
        d_light_np.setZ(100)
        a_light_np = self.character.attachNewNode(a_light)
        d_light.setColor((10, 10, 10, 1))
        a_light.setColor((5, 5, 5, 1))
        d_light_np.setHpr(-60, -30, 10)
        self.character.setLight(d_light_np)
        self.character.setLight(a_light_np)

        point_light = PointLight("point_light")
        point_light_node_path = self.character.attachNewNode(point_light)
        point_light_node_path.setScale(500)
        point_light_node_path.setPos(self.character.getPos())
        point_light_node_path.setZ(self.character.getZ()+30)
        point_light_node_path.setY(self.character.getY() + 100)
        point_light.setColor((50, 50, 50, 1))
        self.character.setLight(point_light_node_path)
        complexpbr.apply_shader(self.character)




