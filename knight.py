from direct.fsm.FSM import FSM
from panda3d.core import *
from direct.actor.Actor import Actor
from player import Player


class Knight(Player):
    def __init__(self, player_num, base):
        self.player_num = player_num
        self.base = base
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
        super().__init__(self.player_num, self.base)
        #self.character.setPos(-100, 0, 0)
        #self.character.setScale(200)
        #self.c_capsule = CollisionSphere(0.5, -0.4, 0.8, 0.25)
        #self.c_segment = CollisionSegment(0, 0.5, 1, 0, -0.5, 1)
        self.ranges = {
            "Attack1": [437.3323516845703, 0.25],
            "Attack2": [414.7734603881836, 0.25],
            "Attack3": [471.92579650878906, 0.25],
            "Attack4": [458.37034606933594, 0.75]}

    '''def special(self, num="1"):
        super().special(num)
        space =0
        self.in_special1 = True

        self.sword4 = self.base.loader.loadModel(f"models/swords/sword5.bam")
        self.sword4.setPos(self.enemy.character.getPos())
        self.sword4.setZ(self.sword4.getZ() + 550)
        self.sword4.setX(self.sword4.getX() - 550)
        self.sword4.setScale(30)
        self.sword4.reparentTo(self.base.render)  ###sword2 = self.base.loader.loadModel(f"models/swords/sword2.bam")
        self.sword4.setHpr(0, 0, 135)


        self.sword5 = self.base.loader.loadModel(f"models/swords/sword6.bam")
        self.sword5.setPos(self.enemy.character.getPos())
        self.sword5.setZ(self.sword5.getZ() + 550)
        self.sword5.setX(self.sword5.getX() + 550)
        self.sword5.setScale(30)
        self.sword5.reparentTo(self.base.render)  ###sword2 = self.base.loader.loadModel(f"models/swords/sword2.bam")
        self.sword5.setHpr(0, 0, -135)
        self.base.taskMgr.add(self.special1_task, "sppecialsz")
    def special1_task(self, task):
        if self.in_special1:
            if task.time<3:
                self.ignore("x")
                dt = self.base.clock.dt
                self.sword5.setPos(self.sword5.getX() -750*dt, self.sword5.getY(), self.sword5.getZ()-500*dt)
                self.sword4.setPos(self.sword4.getX() +750*dt, self.sword4.getY(), self.sword4.getZ()-500*dt)
                if self.calc_abs_distance(self.sword5, self.enemy.character) <= 500 or self.calc_abs_distance(self.sword4, self.enemy.character) <= 500:
                    self.base.taskMgr.doMethodLater(0.3, self.react, 'reaction time')
                    #print("hurt")
            if task.time>3:
                self.sword5.hide()
                self.sword4.hide()
                self.enemy.health -= 25
                self.base.taskMgr.remove("sppecialsz")

            #elif task.time >3:
        #self.in_special1 = False
        return task.cont
    def calc_abs_distance(self, obj1, obj2):
        a = (obj1.getX(), obj1.getY(), obj1.getZ() )
        b = (obj2.getX(), obj2.getY(), obj2.getZ() )
        #print(a, b)
        c = 0
        if len(a) == len(b):
            for i in range(len(a)):
                c += (a[i] - b[i])**2
        c = int(c**0.5)
        #print(c)
        return c'''



