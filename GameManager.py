import pygame

class GameManager():
    def __init__(self, scene):

        self.pauseGame = False

        #Controle da cena
        self.pointSelected = False
        self.playMode = False
        self.pointsPlaced = 0
        self.runTimes = 0
        self.clockTick = 60

        self.speed = 1

        #Scene
        self.scene = scene
        self.clock = scene.clock
        self.events = scene.events
        self.surface = scene.surface

        self.player = scene.player
        self.pointHandler = scene.pointHandler
        self.hud = scene.hudCanvas

        #setando as coisa
        self.pointHandler.gameManager = self

        self.player.gameManager = self
        self.player.pointHandler = self.pointHandler

        self.hud.gameManager = self

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
        if self.events['space']:
            self.TogglePlayMode()

        if self.events['one']:
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
        self.player.rect.x = self.player.startPos[0]
        self.player.rect.y = self.player.startPos[1]

    def TogglePlayMode(self):
        self.playMode = not self.playMode
        if not self.playMode:
            self.RestartLevel()

    def TogglePointSelected(self):
        self.pointSelected = not self.pointSelected