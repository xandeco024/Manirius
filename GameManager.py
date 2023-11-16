import pygame

class GameManager():
    def __init__(self, screen, clock, inputs):
        self.inputs = inputs
        self.screen = screen
        self.clock = clock

        self.pauseGame = False

        #Controle da cena
        self.pointSelected = False
        self.playMode = False
        self.pointsPlaced = 0
        self.runTimes = 0
        self.clockTick = 60

        self.speed = 1

    def SetScene(self, scene):
        self.scene = scene

        self.player = self.scene.player
        self.mapArray = self.scene.mapArray
        self.pointHandler = self.scene.pointHandler
        self.winPos = self.scene.winPos
        self.startPos = self.scene.playerStartPos

    def SimulationSpeedUp(self):
        if self.speed < 3:
            self.speed += 1
            self.clockTick += 60
            self.clock.tick(self.clockTick)
    
    def SimulationSpeedDown(self):
        if self.speed > 1:
            self.speed -= 1
            self.clockTick -= 60
            self.clock.tick(self.clockTick)

    def Update(self):
        if self.inputs['space']:
            self.TogglePlayMode()

        if self.inputs['one']:
            if not self.playMode:
                self.pointSelected = not self.pointSelected

        if not self.pointHandler.pointList:
            self.playMode = False

        if self.playMode:
            self.player.canMove = True

            if self.pointSelected:
                self.pointSelected = False

        else:
            self.player.canMove = False

    def TogglePause(self):
        pass

    def RestartLevel(self):
        self.playMode = False
        self.pointSelected = False
        self.pointHandler.pointList.clear()
        self.player.ReturnToStart()

    def TogglePlayMode(self):
        self.playMode = not self.playMode
        if not self.playMode:
            self.RestartLevel()

    def TogglePointSelected(self):
        self.pointSelected = not self.pointSelected