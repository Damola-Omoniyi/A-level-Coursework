from direct.fsm.FSM import FSM
from panda3d.core import *
from direct.actor.Actor import Actor
from player import Player


class Crypto(Player):
    def __init__(self, player_num, base):
        self.player_num = player_num
        self.base = base
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
        super().__init__(self.player_num, self.base)

        #self.player.setPos(300, 0, 0)
        #self.player.setScale(200)
        #self.c_capsule = CollisionSphere(0.5, -0.4, 0.8, 0.25)
        #self.c_segment = CollisionSegment(0, 0.5, 1, 0, -0.5, 1)
        #self.atk_sound = self.base.loader.loadSfx("models/qubodupPunch/qubodupPunch/qubodupPunch01.ogg")
        self.ranges = {
            "Attack1": [358.362060546875, 0.25],
            "Attack2": [433.4682922363281, 0.25],
            "Attack3": [358.3881530761719, 0.5],
            "Attack4": [282.9663848876953, 0.25]}


    '''def special(self, num="1"):
        super().special("2")
        self.in_special2 = True
        self.fireball = self.base.loader.loadModel(f"models/jack.egg.pz")
        self.fireball.reparentTo(self.base.render)
        self.fireball.setScale(45)
        self.fireball.setPos(self.enemy.player.getPos())
        self.fireball.setZ(self.fireball.getZ()+50)
        self.base.taskMgr.add(self.special2_task, "sppecial")

    def special2_task(self, task):
        if self.in_special2:
            if task.time<3:
                self.ignore("y")
                dt = self.base.clock.dt
                self.fireball.setZ(self.fireball.getZ()+750*dt)
                if abs(self.fireball.getZ()-self.enemy.player.getZ())<= 150 or abs(self.fireball.getX()-self.enemy.player.getX())<= 150:
                    self.base.taskMgr.doMethodLater(0.3, self.react, 'reaction time')
                    #print("hurt")
            if task.time>3:
                self.fireball.hide()
                self.enemy.health -= 25
                self.base.taskMgr.remove("sppecial")
        return task.cont '''
