import pygame, time, sys, asyncio, Objects

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

class Scene(): #CENA BASE PARA CENAS JOGAVEIES E NAO JOGAVEIS.
    def __init__(self, name, surface, clock,  events, sceneManager):
        self.surface = surface
        self.clock = clock
        self.clockTick = 60
        self.events = events
        self.sceneManager = sceneManager
        self.name = name

    def Update(self):
        pass

class SplashScreen(Scene):
    def __init__(self, surface, clock, events, sceneManager):
        super().__init__('splashScreen', surface, clock, events, sceneManager)

        self.sprites = LoadSprites('Assets/Sprites/Splash/reduced')
        self.spriteIndex = 0
        self.speed = 0.3

    def Update(self):
        self.spriteIndex += self.speed

        if self.spriteIndex > len(self.sprites) - 1 or self.events['space']:
            self.sceneManager.LoadScene('mainMenu')

    def Draw(self):        
        self.surface.fill((0, 0, 0)) 
        self.surface.blit(self.sprites[int(self.spriteIndex)], (0, 0))

class MainMenu(Scene):
    def __init__(self, surface, clock, events, sceneManager):
        super().__init__('mainMenu', surface, clock, events, sceneManager)

        pygame.mixer.music.load('Assets/BGM/menu1.mp3')
        #pygame.mixer.music.play(-1)

        self.mainMenuCanvas = MainMenuCanvas(self.surface, self.events, self.sceneManager)

    def Update(self):
        super().Update()
        self.mainMenuCanvas.Update()

    def Draw(self):
        self.surface.fill((0, 0, 0))
        self.mainMenuCanvas.DrawMenu()

class PlayableScene(Scene): #CENA JOGAVEL
    def __init__(self, name, playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager):

        super().__init__(name, surface, clock, events, sceneManager)

        #Scene basics
        self.playerStartPos = playerStartPos
        self.winPos = winPos
        self.nextLevel = nextLevel
        self.mapArray = mapArray

        self.complete = False

        #game scene
        self.gameSurface = pygame.Surface((640, 640)).convert_alpha()

        #Scene objects

        self.level = Tilemap.Level(mapArray, "Assets/Sprites/Tileset/tileset.png")
        self.background = Background("Assets/Sprites/UI/background.jpg", [-0.5, -0.5])
        self.pointHandler = PointHandler(self.mapArray)
        self.player = Player(self.playerStartPos)

        self.hudCanvas = HUDCanvas()
        self.levelCompleteCanvas = LevelCompleteCanvas()

        self.gameManager = GameManager(self)

        self.lasers = []
        self.buttons = []
        self.portals = []

    def HandleProgess(self):
        if self.player.rect.x == self.winPos[0] and self.player.rect.y == self.winPos[1]:
            self.complete = True

        if self.complete:
            self.levelCompleteCanvas.PlayLevelCompleteSFX()

    def Draw(self, surface):
        self.background.DrawBackground(surface)

        self.level.Draw(self.gameSurface)
        self.pointHandler.Draw(self.gameSurface)

        self.player.Draw(self.gameSurface)

        surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(surface)

        if self.complete:
            self.levelCompleteCanvas.Draw(surface)

    def Update(self):
        super().Update()
        self.HandleProgess()

        self.gameManager.Update()
        self.pointHandler.Update()
        self.player.Update()
        self.hudCanvas.Update()

        if self.buttons:
            for button in self.buttons:
                button.Update()

        if self.lasers:
            for laser in self.lasers:
                laser.Update()

        if self.complete:
            self.levelCompleteCanvas.Update()

class Level1(PlayableScene):
    def __init__(self, surface, clock, events, sceneManager):

        #Level 1 basics
        playerStartPos = (2*64, 8*64)
        winPos = (8*64, 8*64)
        nextLevel = 'level2'

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

        #Particularidades do lvl

        #self.decoTable = Objects.DecorativeObject('Assets/Sprites/Objects/table.png', (128, 64), (128, 64), -180)
        #self.decoPanel = Objects.DecorativeObject('Assets/Sprites/Objects/panel.png', (64, 64), (64, 0), 90)
        #self.decoNiche = Objects.DecorativeObject('Assets/Sprites/Objects/nicho em ingles.png', (64, 64), (256, 0), 0)
        #self.decoPc = Objects.DecorativeObject('Assets/Sprites/Objects/pc.png', (64, 64), (512-128, 0), 0)

        super().__init__('level1', playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        self.surface.fill((0, 0, 0))
        super().Draw(self.surface)

class Level2(PlayableScene):
    def __init__(self, surface, clock, events, sceneManager):

        #level 2 basics
        playerStartPos = (2*64, 8*64)
        winPos = (7*64, 1*64)
        nextLevel = 'level3'

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


        super().__init__('level2',playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

        #Particularidades do lvl

        self.lasers = [
            Objects.Laser((320, 384), 90, True, self.gameManager)
            ]
        
        self.buttons = [
            Objects.Button((128, 64), self.lasers, self.gameManager)
        ]

    def Update(self):
        super().Update()

    def Draw(self):
        self.surface.fill((0, 0, 0))
        #super().Draw(self.surface) #requer organizacao na renderizacao e tals

        self.background.DrawBackground(self.surface)

        self.level.Draw(self.gameSurface)

        for button in self.buttons:
            button.Draw(self.gameSurface)

        for laser in self.lasers:
            laser.Draw(self.gameSurface)

        self.pointHandler.Draw(self.gameSurface)

        self.player.Draw(self.gameSurface)

        self.surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(self.surface)

        if self.complete:
            self.levelCompleteCanvas.Draw(self.surface)

class Level3(PlayableScene):
    def __init__(self, surface, clock, events, sceneManager):

        #level 3 basics
        playerStartPos = (8 * 64, 1 * 64)
        winPos = (64, 8*64)
        nextLevel = 'level4'

        mapArray = [
            [31,22,22,22,22,22,22,22,22,33],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,1,2,53],
            [13,42,42,42,42,42,42,11,12,12],
            [13,42,42,42,42,1,2,53,12,12],
            [13,42,42,42,42,11,12,12,12,12],
            [13,42,42,1,2,53,12,12,12,12],
            [13,42,42,11,12,12,12,12,12,12],
            [51,52,2,53,12,12,12,12,12,12]
        ]

        #Particularidades do lvl

        super().__init__('level3', playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

        self.lasers = [
            Objects.Laser((7 * 64, 64), 90, True, self.gameManager),
            Objects.Laser((7 * 64, 128), 90, True, self.gameManager),
            Objects.Laser((5 * 64, 64), 90, True, self.gameManager),
            Objects.Laser((5 * 64, 128), 90, True, self.gameManager),
            Objects.Laser((5 * 64, 192), 90, True, self.gameManager),
            Objects.Laser((5 * 64, 256), 90, True, self.gameManager),
            Objects.Laser((3 * 64, 64), 90, True, self.gameManager),
            Objects.Laser((3 * 64, 128), 90, True, self.gameManager),
            Objects.Laser((3 * 64, 192), 90, True, self.gameManager),
            Objects.Laser((3 * 64, 256), 90, True, self.gameManager),
            Objects.Laser((3 * 64, 320), 90, True, self.gameManager),
            Objects.Laser((3 * 64, 384), 90, True, self.gameManager),
            Objects.Laser((1 * 64, 7 * 64), 0, True, self.gameManager),
            Objects.Laser((2 * 64, 7 * 64), 0, True, self.gameManager)
        ]
    
        self.buttons = [
            Objects.Button((8 * 64, 128), [self.lasers[0], self.lasers[1]], self.gameManager),
            Objects.Button((6 * 64, 256), [self.lasers[2],self.lasers[3], self.lasers[4], self.lasers[5]], self.gameManager),
            Objects.Button((4 * 64, 384), [self.lasers[6], self.lasers[7], self.lasers[8], self.lasers[9], self.lasers[10], self.lasers[11]], self.gameManager),
            Objects.Button((1 * 64, 64), [self.lasers[12], self.lasers[13]], self.gameManager)
        ]

    def Update(self):
        super().Update()

    def Draw(self):
        self.surface.fill((0, 0, 0))
        #super().Draw(self.surface) #requer organizacao na renderizacao e tals

        self.background.DrawBackground(self.surface)

        self.level.Draw(self.gameSurface)

        for button in self.buttons:
            button.Draw(self.gameSurface)

        for laser in self.lasers:
            laser.Draw(self.gameSurface)

        self.pointHandler.Draw(self.gameSurface)

        self.player.Draw(self.gameSurface)

        self.surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(self.surface)

        if self.complete:
            self.levelCompleteCanvas.Draw(self.surface)

class Level4(PlayableScene):
    def __init__(self, surface, clock, events, sceneManager):

        #level 4 basics
        playerStartPos = (64, 512)
        winPos = (8*64, 8*64)
        nextLevel = 'level4'

        mapArray = [
            [31,22,22,22,22,22,22,22,22,33],
            [13,20,42,42,42,30,42,30,42,11],
            [13,42,42,42,42,30,42,30,42,43],
            [13,42,42,42,42,30,42,30,42,11],
            [13,42,42,42,75,95,95,95,95,11],
            [13,42,42,10,71,10,42,42,42,11],
            [13,42,42,42,71,42,42,42,42,11],
            [13,42,42,42,71,42,42,42,42,11],
            [13,42,42,42,71,42,42,42,10,11],
            [51,2,2,2,2,2,2,2,2,53]
        ]

        #Particularidades do lvl

        super().__init__('level4', playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        self.surface.fill((0, 0, 0))
        super().Draw(self.surface)

class Level5(PlayableScene):
    def __init__(self, surface, clock, events, sceneManager):

        #level 5 basics
        playerStartPos = (64, 512)
        winPos = (8*64, 8*64)
        nextLevel = 'mainMenu'

        mapArray = [
            [31,22,22,22,22,22,22,22,22,33],
            [13,20,42,42,42,42,42,42,42,11],
            [13,20,42,42,42,42,42,42,42,11],
            [13,95,95,95,95,95,95,95,95,11],
            [13,20,42,40,42,42,40,42,20,11],
            [51, 2, 2, 3,42,42, 1, 2, 2,53],
            [12,12,12,13,42,42,11,12,12,12],
            [12,12,12,13,42,42,11,12,12,12],
            [12,12,12,51, 2,55,53,12,12,12],
            [12,12,12,12,12,12,12,12,12,12]
        ]

        #Particularidades do lvl

        super().__init__('level5', playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        self.surface.fill((0, 0, 0))
        super().Draw(self.surface)

class SceneManager():
    def __init__(self, initialScene):
        self.currentScene = self.LoadScene(initialScene)

    def LoadScene(self, scene):
        #self.currentScene = scene

        if scene == 'splashScreen':
            self.currentScene = SplashScreen(screen, clock, events, self)

        elif scene == 'mainMenu':
            self.currentScene = MainMenu(screen, clock, events, self)

        elif scene == 'level1':
            self.currentScene = Level1(screen, clock, events, self)

        elif scene == 'level2':
            self.currentScene = Level2(screen, clock, events, self)

        elif scene == 'level3':
            self.currentScene = Level3(screen, clock, events, self)

        elif scene == 'level4':
            self.currentScene = Level4(screen, clock, events, self)

        elif scene == 'level5':
            self.currentScene = Level5(screen, clock, events, self)

        return self.currentScene

    def GetScene(self):
        return self.currentScene
#region Heliópolis

events = {'space': False, 'rightClick': False, 'leftClick': False, 'escape': False, 'tab': False, 'one': False}

sceneManager = SceneManager('level2')

#splashScreen = SplashScreen(screen, events, sceneManager)

#mainMenu = MainMenu(screen, events, sceneManager)

#level1 = Level1(screen, clock, events, sceneManager)
#level2 = Level2(screen, clock, events, sceneManager)
#level3 = Level3(screen, clock, events, sceneManager)
#level4 = Level4(screen, clock, events, sceneManager)
#level5 = Level5(screen, clock, events, sceneManager)

#scenes = {'splashScreen': splashScreen, 'mainMenu': mainMenu, 'level1': level1, 'level2': level2, 'level3': level3, 'level4': level4, 'level5': level5}

async def main():
    while True:
        EventCheck(events)
        #scenes[sceneManager.GetScene()].Update()
        #scenes[sceneManager.GetScene()].Draw()
        #if sceneManager.GetScene() != 'mainMenu' and sceneManager.GetScene() != 'splashScreen':
        #    clock.tick(scenes[sceneManager.GetScene()].gameManager.clockTick)
        #else:
        #    clock.tick(60)

        sceneManager.GetScene().Update()
        sceneManager.GetScene().Draw()
        clock.tick(sceneManager.GetScene().clockTick)

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())

#endregion