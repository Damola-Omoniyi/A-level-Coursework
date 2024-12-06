from direct.showbase.ShowBase import ShowBase
from gui import GUI
def mint(mine):
    print(mine,"minted")

mint(mine = 22)
class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.UI = GUI(self)
        self.UI.title_menu()


base = Main()
base.run()