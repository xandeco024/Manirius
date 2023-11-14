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

    def HandleSimulationSpeed(self):
        if(self.clockTick == 60):
            self.SimulationSpeed2()
        elif(self.clockTick == 120):
            self.SimulationSpeed3()
        elif(self.clockTick == 180):
            self.SimulationSpeed1()

    def SimulationSpeed1(self):
        self.clock.tick(60)
        self.clock.tick(self.clockTick)
    
    def SimulationSpeed2(self):
        self.clock.tick(120)
        self.clock.tick(self.clockTick)
    
    def SimulationSpeed3(self):
        self.clock.tick(180)
        self.clock.tick(self.clockTick)

    def Update(self):
        if self.inputs['tab']:
            self.HandleSimulationSpeed()

        if self.inputs['space']:
            self.TogglePlayMode()

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

    def TogglePlayMode(self):
        self.playMode = not self.playMode
        if not self.playMode:
            self.Restart()