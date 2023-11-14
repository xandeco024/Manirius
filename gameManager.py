import pygame

class GameManager():
    def __init__(self, screen, clock, inputs):
        self.inputs = inputs
        self.screen = screen
        self.clock = clock

        self.pauseGame = False

        self.winPos = [0,0]
        self.startPos = [0,0]

        #Controle da 
        self.pointSelected = False
        self.playMode = False
        self.pointsPlaced = 0
        self.runTimes = 0
        self.clockTick = 60

    def NewScene(self, player, mapArray, pointHandler, winPos):
        self.pointsPlaced = 0
        self.runTimes = 0
        #self.clockTick = 60
        self.player = player
        self.mapArray = mapArray
        self.pointHandler = pointHandler
        self.winPos = winPos

    def HandlePlaySpeed(self):
        if self.inputs['tab']:
            self.clockTick += 60
            
        if self.clockTick > 180:
            self.clockTick = 60

        self.clock.tick(self.clockTick)

    def Update(self):
        self.HandlePlaySpeed()

        if self.inputs['space']:
            self.playMode = not self.playMode
            if not self.playMode:
                self.Restart()

        if self.inputs['one']:
            if not self.playMode:
                self.pointSelected = not self.pointSelected

        if self.playMode and self.pointSelected:
            self.pointSelected = False

        if not self.pointHandler.pointList:
            self.playMode = False

    def Restart(self):
        self.playMode = False
        self.pointSelected = False
        self.pointHandler.pointList.clear()
        self.player.ReturnToStart()