import pygame

class GameManager():
    def __init__(self, inputs, player, clock):
        self.inputs = inputs
        self.player = player
        self.clock = clock
        self.clockTick = 60

    def NewScene(self):
        pass

    def HandlePlaySpeed(self):
        if self.inputs['tab']:
            self.clockTick += 60
            
        if self.clockTick >= 180:
            self.clockTick = 60

        self.clock.tick(self.clockTick)

    def Update(self):
        self.HandlePlaySpeed()
