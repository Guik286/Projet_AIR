from BrouillonBattleSys.KeysManager import *

class controleBattle:
    def __init__(self):
        self.manager = KeysManager()
        self.input = False
        print(self.manager._key_map)

    def check_input(self):
        if self.manager.is_key_down("start"):
           self.input = True 
        