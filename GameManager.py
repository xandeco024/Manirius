import pygame

class GameManager():
    def __init__(self, level):

        self.pauseGame = False

        #Controle da cena
        self.pointSelected = False
        self.playMode = False
        self.pointsPlaced = 0
        self.runTimes = 0
        self.clockTick = 60
        self.speed = 1

        self.playerLastPlayPos = None

        #Scene
        self.level = level
        self.clock = level.clock
        self.events = level.events
        self.surface = level.surface

        self.player = level.player
        self.pointHandler = level.pointHandler
        self.hud = level.hudCanvas
        self.levelComplete = level.levelCompleteCanvas

        #setando as coisa
        self.pointHandler.gameManager = self

        self.player.gameManager = self
        self.player.pointHandler = self.pointHandler

        self.hud.gameManager = self

        self.levelComplete.gameManager = self

    def SimulationSpeedUp(self):
        if self.speed < 3:
            self.speed += 1
            self.level.clockTick += 60
    
    def SimulationSpeedDown(self):
        if self.speed > 1:
            self.speed -= 1
            self.level.clockTick -= 60

    def Update(self):
        if self.playMode:
            if not self.player.dead:
                self.player.canMove = True
            if self.pointSelected:
                self.pointSelected = False

        else:
            self.player.canMove = False

        if self.playMode and not self.pointHandler.pointList:
            self.playMode = False

    def TogglePauseGame(self):
        self.pauseGame = not self.pauseGame

    def RestartLevel(self):
        self.playMode = False
        self.pointSelected = False
        self.pointHandler.pointList.clear()
        self.player.rect.x = self.player.startPos[0]
        self.player.rect.y = self.player.startPos[1]
        self.player.direction = [0,0]
        self.player.dead = False
        self.player.rotation = 0
        self.player.canMove = False

        for laser in self.level.lasers:
            if laser.initiallyActive:
                laser.Enable()
            else:
                laser.Disable()

        for button in self.level.buttons:
            if button.pressed:
                button.pressed = False

        if self.level.complete:
            self.level.complete = False

    def TogglePlayMode(self):
        self.playMode = not self.playMode
        if self.playMode:
            self.runTimes += 1

    def TogglePointSelected(self):
        self.pointSelected = not self.pointSelected