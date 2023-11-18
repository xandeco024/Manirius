import pygame, time, sys, asyncio

from ROBB9 import Player
from Utilities import *
from GameManager import GameManager
from UI import *
from PointHandler import PointHandler
import Tilemap

#region Inicio do codigo
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Mánirius")
clock = pygame.time.Clock()
#endregion

#region Global Variables
verminVibes = "Fonts/Vermin Vibes 1989.ttf"
kenneyPixel = "Fonts/Kenney Pixel.ttf"
#endregion
        
class SplashScreen():
    def __init__(self, surface, inputs, sceneManager):
        self.inputs = inputs
        self.surface = surface
        self.sceneManager = sceneManager

        self.sprites = LoadSprites('Sprites/Splash/reduced')
        self.spriteIndex = 0
        self.speed = 0.3

    def Update(self):
        self.spriteIndex += self.speed

        if self.spriteIndex > len(self.sprites) - 1 or self.inputs['space']:
            self.sceneManager.LoadScene('mainMenu')

    def Draw(self):        
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.sprites[int(self.spriteIndex)], (0, 0))

class MainMenu():
    def __init__(self, surface, inputs, sceneManager):   
        pygame.mixer.music.load('BGM/menu1.mp3')
        pygame.mixer.music.play(-1)
        self.surface = surface
        self.sceneManager = sceneManager
        self.inputs = inputs
        self.mainMenuCanvas = MainMenuCanvas(self.surface, self.inputs, self.sceneManager)

    def Update(self):
        self.mainMenuCanvas.Update()

    def Draw(self):
        self.surface.fill((0, 0, 0))
        self.mainMenuCanvas.DrawMenu()

class Scene():
    def __init__(self, playerStartPos, winPos, mapArray, sceneManager):

        self.gameManager = GameManager(screen, clock, inputs)

        self.sceneManager = sceneManager

        self.screen = self.gameManager.screen
        self.clock = self.gameManager.clock

        self.playerStartPos = playerStartPos
        self.winPos = winPos

        self.mapArray = mapArray

        self.complete = False

        self.background = Background("Sprites/UI/background.jpg", [-0.5, -0.5])

        self.hudCanvas = HUDCanvas(self.gameManager)
        self.pointHandler = PointHandler(self.mapArray, self.gameManager)
        self.player = Player(self.playerStartPos, self.pointHandler)

        self.level = Tilemap.Level(mapArray, "Sprites/Tileset/tileset.png")

        self.gameSurface = pygame.Surface((640, 640)).convert_alpha()
        self.gameManager.SetScene(self)

    def CheckProgress(self):
        if self.player.rect.x == self.winPos[0] and self.player.rect.y == self.winPos[1]:
            self.complete = True

    def SceneUpdate(self):
        self.CheckProgress()

class Scene1(Scene):
    def __init__(self, sceneManager):
        playerStartPos = (2*64, 8*64)
        winPos = (8*64, 8*64)
        mapArray = [
            [31,22,22,35,25,22,35,22,33,12],
            [13,42,42,42,42,42,42,42,11,12],
            [16,42,42,42,42,42,42,42,11,12],
            [13,42,42,42,42,42,42,42,11,12],
            [13,42,42,42,61,42,42,42,11,12],
            [44,42,42,42,71,42,42,42,11,12],
            [44,42,42,42,71,42,42,42,11,12],
            [16,42,42,42,71,42,42,42,21,33],
            [13,42,42,42,71,42,42,42,42,43],
            [51, 2, 5, 2,62, 2, 2, 2, 2,53]
        ]

        super().__init__(playerStartPos, winPos, mapArray, sceneManager)

    def Update(self):
        self.SceneUpdate()

        self.gameManager.Update()
        self.pointHandler.Update()
        self.player.Update()
        self.hudCanvas.Update()

        if self.complete:
            self.sceneManager.LoadScene('scene2')

    def Draw(self):
        screen.fill((0, 0, 0))

        self.background.DrawBackground(screen)

        self.level.Draw(self.gameSurface)
        self.pointHandler.Draw(self.gameSurface)
        self.player.Draw(self.gameSurface)
        self.screen.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(screen)

class Scene2(Scene):
    def __init__(self, sceneManager):
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

        super().__init__(playerStartPos, winPos, mapArray, sceneManager)

        self.button1 = Button((2*64, 1*64), 'batata')

    def Update(self):
        screen.fill((0, 0, 0))

        self.SceneUpdate()

        self.level.DrawLevel()

        self.button1.Draw(screen)
        self.pointHandler.Update(self.screen, self.player.rect, self.inputs['leftClick'], self.inputs['rightClick'],self.gridHandler.valid, True)
        self.player.Update(self.screen, self.pointHandler, self.playMode)

        pygame.display.update()

        if self.complete:
            #self.levelCompleteCanvas.Draw(screen, self.inputs['leftClick'])
            self.sceneManager.LoadScene('scene3')

class Scene3(Scene):
    def __init__(self, sceneManager):
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

        super().__init__(playerStartPos, winPos, mapArray, sceneManager)

    def Update(self):
        screen.fill((0, 0, 0))

        self.SceneUpdate()

        self.level.DrawLevel()

        if self.itemSelected:
            if self.pointHandler.pointList:
                self.gridHandler.Update(self.screen, self.pointHandler.pointList[len(self.pointHandler.pointList) - 1].rect)
            else:
                self.gridHandler.Update(self.screen, self.player.rect)

        self.pointHandler.Update(self.screen, self.player.rect, self.inputs['leftClick'], self.inputs['rightClick'],self.gridHandler.valid, True)
        self.player.Update(self.screen, self.pointHandler, self.playMode)

        if self.complete:
            #self.levelCompleteCanvas.Draw(screen, self.inputs['leftClick'])
            self.sceneManager.LoadScene('mainMenu')

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, link): 
        self.pos = pos
        self.link = link
        self.pressed = False

        self.sprites = CutSpritesheet('Sprites/Objects/button.png', (64, 64))

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
    def __init__(self, initialScene):
        self.currentScene = initialScene

    def LoadScene(self, scene):
        self.currentScene = scene
    
    def GetScene(self):
        return self.currentScene

#region Heliópolis

inputs = {'space': False, 'rightClick': False, 'leftClick': False, 'escape': False, 'tab': False, 'one': False}

sceneManager = SceneManager('splashScreen')

splashScreen = SplashScreen(screen, inputs, sceneManager)

mainMenu = MainMenu(screen, inputs, sceneManager)

scene1 = Scene1(sceneManager)
scene2 = Scene2(sceneManager)
scene3 = Scene3(sceneManager)

scenes = {'splashScreen': splashScreen, 'mainMenu': mainMenu, 'scene1': scene1, 'scene2': scene2, 'scene3': scene3}

async def main():
    while True:
        EventCheck(inputs)
        scenes[sceneManager.GetScene()].Update()
        scenes[sceneManager.GetScene()].Draw()
        if sceneManager.GetScene() != 'mainMenu' and sceneManager.GetScene() != 'splashScreen':
            clock.tick(scenes[sceneManager.GetScene()].gameManager.clockTick)
        else:
            clock.tick(60)

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())

#endregion