import pygame
import time
import sys

from ROBB9 import Player
from Utilities import *
from GameManager import GameManager
from UI import *
from PointHandler import PointHandler
from GridHandler import GridHandler

#region Inicio do codigo
pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Mánirius")
clock = pygame.time.Clock()
#endregion

#region Global Variables
verminVibes = "Fonts/Vermin Vibes 1989.ttf"
kenneyPixel = "Fonts/Kenney Pixel.ttf"
#endregion

class Level():
    def __init__(self, map, tilesetSprite, screen):

        super().__init__()
        self.map = map
        self.tilesetSprite = tilesetSprite
        self.screen = screen

    def DrawLevel(self):

        tileRects = []
        tiles = []

        tilemap = pygame.Surface((640, 640))

        tiles.insert(0, pygame.Surface((64,64)).convert_alpha())

        sprites = CutSpritesheet(self.tilesetSprite, 64, 64)
        tiles.extend(sprites)

        tileWidth = 64
        tileHeight = 64
        for y, row in enumerate(self.map):
            for x, tileIndex in enumerate(row):
                tilemap.blit(tiles[tileIndex], (x * tileWidth, y * tileHeight))
                if tileIndex != 0 and tileIndex != 42:
                    tileRects.append(pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
        
        self.screen.blit(tilemap, (0,0))
        
class MainMenu():
    def __init__(self, screen, inputs, sceneManager):
        self.screen = screen

        #self.backgroundSprite = pygame.image.load("Sprites/UI/background.jpg")
        #self.background = Background(self.backgroundSprite, screen, [-1, -1])

        #self.logo = pygame.image.load("Sprites/UI/logo.png").convert_alpha()

        self.sceneManager = sceneManager

        self.inputs = inputs

        #self.startButton = UIButton("START", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 300), self.OnStartBtnClick)
        #self.settingsButton = UIButton("SETTI  NGS", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 400), sys.exit)
        #self.quitButton = UIButton("QUIT", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 500), sys.exit)

        self.mainMenuCanvas = MainMenuCanvas(screen, inputs, sceneManager)



    def Update(self):
        screen.fill((0, 0, 0))
        self.mainMenuCanvas.Update()

class Scene():
    def __init__(self, playerStartPos, winPos, mapArray, sceneManager, gameManager):

        self.gameManager = gameManager
        self.sceneManager = sceneManager

        self.screen = gameManager.screen
        self.clock = gameManager.clock

        self.playerStartPos = playerStartPos
        self.winPos = winPos

        self.mapArray = mapArray

        self.complete = False

        self.hudCanvas = HUDCanvas(self.gameManager)
        self.pointHandler = PointHandler(self.gameManager)
        self.tileHandler = GridHandler(self.mapArray, self.gameManager)
        self.player = Player(self.playerStartPos)
        self.level = Level(mapArray, "Sprites/Tileset/tileset.png", screen)

    def CheckProgress(self):
        if self.player.rect.x == self.winPos[0] and self.player.rect.y == self.winPos[1]:
            self.complete = True

    def SceneUpdate(self):

        self.CheckProgress()

class Scene1(Scene):
    def __init__(self, sceneManager, gameManager):
        playerStartPos = (2*64, 8*64)
        winPos = (8*64, 8*64)
        mapArray = [
            [31,22,22,22,22,22,22,22,33,12],
            [13,42,42,42,42,42,42,42,11,12],
            [13,42,42,42,42,42,42,42,11,12],
            [13,42,42,42,42,42,42,42,11,12],
            [13,42,42,42,61,42,42,42,11,12],
            [13,42,42,42,71,42,42,42,11,12],
            [13,42,42,42,71,42,42,42,11,12],
            [13,42,42,42,71,42,42,42,21,33],
            [13,42,42,42,71,42,42,42,42,43],
            [51, 2, 2, 2,62, 2, 2, 2, 2,53]
        ]

        super().__init__(playerStartPos, winPos, mapArray, sceneManager, gameManager)

    def Update(self):
        screen.fill((0, 0, 0))

        self.SceneUpdate()

        self.level.DrawLevel()

        if self.gameManager.pointSelected:
            if self.pointHandler.pointList:
                self.tileHandler.Update(self.pointHandler.pointList[len(self.pointHandler.pointList) - 1].rect)
            else:
                self.tileHandler.Update(self.player.rect)

        self.pointHandler.Update(self.tileHandler.valid)
        self.player.Update(self.screen, self.pointHandler, self.gameManager.playMode)

        self.hudCanvas.Update()
        self.hudCanvas.DrawHUD()

        pygame.display.update()

        if self.complete:
            self.sceneManager.LoadScene('scene2')

class Scene2(Scene):
    def __init__(self, sceneManager, gameManager):
        winPos = (7*64, 1*64)
        playerStartPos = (2*64, 8*64)
        mapArray = [
            [31,22,22,22,22,22,22,32,22,33],
            [13,42,42,42,42,71,42,42,42,11],
            [13,42,42,42,42,71,42,42,42,11],
            [13,96,42,94,95,92,42,42,42,11],
            [13,42,42,42,42,71,42,42,42,11],
            [13,42,42,42,42,81,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42, 1, 2, 2, 2,53],
            [13,42,42,42,42,11,12,12,12,12],
            [51, 2, 2, 2, 2,53,12,12,12,12]
        ]

        super().__init__(playerStartPos, winPos, mapArray, sceneManager, gameManager)

        self.button1 = Button((2*64, 1*64), 'batata')

    def Update(self):
        screen.fill((0, 0, 0))

        self.SceneUpdate()

        self.level.DrawLevel()

        self.button1.Draw(screen)

        if self.itemSelected:
            if self.pointHandler.pointList:
                self.tileHandler.Update(self.screen, self.pointHandler.pointList[len(self.pointHandler.pointList) - 1].rect)
            else:
                self.tileHandler.Update(self.screen, self.player.rect)

        self.pointHandler.Update(self.screen, self.player.rect, self.inputs['leftClick'], self.inputs['rightClick'],self.tileHandler.valid, True)
        self.player.Update(self.screen, self.pointHandler, self.playMode)

        pygame.display.update()

        if self.complete:
            #self.levelCompleteCanvas.Draw(screen, self.inputs['leftClick'])
            self.sceneManager.LoadScene('scene3')

class Scene3(Scene):
    def __init__(self, sceneManager, gameManager):
        playerStartPos = (64, 128)
        winPos = (8*64, 8*64)
        mapArray = [
            [31,22,22,22,22,22,22,22,22,33],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42, 1, 2,53],
            [13,42,42,42,42,42,42,11,12,12],
            [13,42,42,42,42, 1, 2,53,12,12],
            [13,42,42,42,42,11,12,12,12,12],
            [13,42,42, 1, 2,53,12,12,12,12],
            [13,42,42,11,12,12,12,12,12,12],
            [51,52,52,53,12,12,12,12,12,12]
        ]

        super().__init__(playerStartPos, winPos, mapArray, sceneManager, gameManager)

    def Update(self):
        screen.fill((0, 0, 0))

        self.SceneUpdate()

        self.level.DrawLevel()

        if self.itemSelected:
            if self.pointHandler.pointList:
                self.tileHandler.Update(self.screen, self.pointHandler.pointList[len(self.pointHandler.pointList) - 1].rect)
            else:
                self.tileHandler.Update(self.screen, self.player.rect)

        self.pointHandler.Update(self.screen, self.player.rect, self.inputs['leftClick'], self.inputs['rightClick'],self.tileHandler.valid, True)
        self.player.Update(self.screen, self.pointHandler, self.playMode)

        pygame.display.update()

        if self.complete:
            #self.levelCompleteCanvas.Draw(screen, self.inputs['leftClick'])
            self.sceneManager.LoadScene('mainMenu')

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, link):
        self.pos = pos
        self.link = link
        self.pressed = False

        self.sprites = CutSpritesheet('Sprites/Objects/button.png', 64, 64)

        self.image = self.sprites[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

        super().__init__()

    def Press(self):
        self.pressed = True
        self.image = self.sprites[1]
        #self.link.Action()

    def Draw(self, screen):
        screen.blit(self.image, (self.pos[0], self.pos[1]))

    def Update(self):
        pass

class SceneManager():
    def __init__(self, initialScene, gameManager):
        self.currentScene = initialScene
        self.gameManager = gameManager

    def LoadScene(self, scene):
        self.currentScene = scene
    
    def GetScene(self):
        return self.currentScene

#region Heliópolis

inputs = {'space': False, 'rightClick': False, 'leftClick': False, 'escape': False, 'tab': False, 'one': False}

gameManager = GameManager(screen, clock, inputs)
sceneManager = SceneManager('mainMenu', gameManager)

mainMenu = MainMenu(screen, inputs, sceneManager)

scene1 = Scene1(sceneManager, gameManager)
scene2 = Scene2(sceneManager, gameManager)
scene3 = Scene3(sceneManager, gameManager)

scenes = {'mainMenu': mainMenu, 'scene1': scene1, 'scene2': scene2, 'scene3': scene3}

while True:
    EventCheck(inputs)
    scenes[sceneManager.GetScene()].Update()
    if sceneManager.GetScene() != 'mainMenu':
        gameManager.NewScene(scenes[sceneManager.GetScene()].player, scenes[sceneManager.GetScene()].mapArray, scenes[sceneManager.GetScene()].pointHandler, scenes[sceneManager.GetScene()].winPos)
        gameManager.Update()
    clock.tick(gameManager.clockTick)
    pygame.display.update()

#endregion