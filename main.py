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


class Scene(): #CENA BASE PARA CENAS JOGAVEIES E NAO JOGAVEIS.
    def __init__(self, surface, clock,  events, sceneManager):
        self.surface = surface
        self.clock = clock
        self.events = events
        self.sceneManager = sceneManager

    def Update(self):
        pass

class PlayableScene(Scene): #CENA JOGAVEL
    def __init__(self, playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager):

        super().__init__(surface, clock, events, sceneManager)

        #Scene basics
        self.playerStartPos = playerStartPos
        self.winPos = winPos
        self.nextLevel = nextLevel
        self.mapArray = mapArray

        self.complete = False

        #game scene
        self.gameSurface = pygame.Surface((640, 640)).convert_alpha()

        #Scene objects

        self.level = Tilemap.Level(mapArray, "Sprites/Tileset/tileset.png")
        self.background = Background("Sprites/UI/background.jpg", [-0.5, -0.5])
        self.hudCanvas = HUDCanvas()
        self.pointHandler = PointHandler(self.mapArray)
        self.player = Player(self.playerStartPos)

        self.gameManager = GameManager(self)

    def HandleProgess(self):
        if self.player.rect.x == self.winPos[0] and self.player.rect.y == self.winPos[1]:
            self.complete = True

        if self.complete and events['space']: #Implementar logica pra passar de fase
            self.sceneManager.LoadScene(self.nextLevel)

    def Update(self):
        super().Update()
        self.HandleProgess()

        self.gameManager.Update()
        self.pointHandler.Update()
        self.player.Update()
        self.hudCanvas.Update()

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

        self.decoTable = Objects.DecorativeObject('Sprites/Objects/table.png', (128, 64), (128, 64), -180)
        self.decoPanel = Objects.DecorativeObject('Sprites/Objects/panel.png', (64, 64), (64, 0), 90)
        self.decoNiche = Objects.DecorativeObject('Sprites/Objects/nicho em ingles.png', (64, 64), (256, 0), 0)
        self.decoPc = Objects.DecorativeObject('Sprites/Objects/pc.png', (64, 64), (512-128, 0), 0)

        super().__init__(playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        screen.fill((0, 0, 0))

        self.background.DrawBackground(screen)

        self.level.Draw(self.gameSurface)
        self.pointHandler.Draw(self.gameSurface)

        '''self.decoTable.Draw(self.gameSurface)
        self.decoPanel.Draw(self.gameSurface)
        self.decoNiche.Draw(self.gameSurface)
        self.decoPc.Draw(self.gameSurface)'''


        self.player.Draw(self.gameSurface)

        self.surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(screen)

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

        #Particularidades do lvl

        super().__init__(playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        screen.fill((0, 0, 0))

        self.background.DrawBackground(screen)

        self.level.Draw(self.gameSurface)
        self.pointHandler.Draw(self.gameSurface)
        self.player.Draw(self.gameSurface)
        self.surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(screen)

class Level3(PlayableScene):
    def __init__(self, surface, clock, events, sceneManager):

        #level 3 basics
        playerStartPos = (64, 12)
        winPos = (8*64, 8*64)
        nextLevel = 'level4'

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

        #Particularidades do lvl

        super().__init__(playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        screen.fill((0, 0, 0))

        self.background.DrawBackground(screen)

        self.level.Draw(self.gameSurface)
        self.pointHandler.Draw(self.gameSurface)
        self.player.Draw(self.gameSurface)
        self.surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(screen)

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

        super().__init__(playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        screen.fill((0, 0, 0))

        self.background.DrawBackground(screen)

        self.level.Draw(self.gameSurface)
        self.pointHandler.Draw(self.gameSurface)
        self.player.Draw(self.gameSurface)
        self.surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(screen)

class Level5(PlayableScene):
    def __init__(self, surface, clock, events, sceneManager):

        #level 5 basics
        playerStartPos = (64, 512)
        winPos = (8*64, 8*64)
        nextLevel = 'mainMenu'

        mapArray = [
            [31,22,22,22,22,22,22,22,22,33],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [13,42,42,42,42,42,42,42,42,11],
            [51,2,2,2,2,2,2,2,2,53]
        ]

        #Particularidades do lvl

        super().__init__(playerStartPos, winPos, nextLevel, mapArray, surface, clock, events, sceneManager)

    def Update(self):
        super().Update()

    def Draw(self):
        screen.fill((0, 0, 0))

        self.background.DrawBackground(screen)

        self.level.Draw(self.gameSurface)
        self.pointHandler.Draw(self.gameSurface)
        self.player.Draw(self.gameSurface)
        self.surface.blit(self.gameSurface, (320,0))

        self.hudCanvas.DrawHUD(screen)

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

events = {'space': False, 'rightClick': False, 'leftClick': False, 'escape': False, 'tab': False, 'one': False}

sceneManager = SceneManager('splashScreen')

splashScreen = SplashScreen(screen, events, sceneManager)

mainMenu = MainMenu(screen, events, sceneManager)

level1 = Level1(screen, clock, events, sceneManager)
level2 = Level2(screen, clock, events, sceneManager)
level3 = Level3(screen, clock, events, sceneManager)
level4 = Level4(screen, clock, events, sceneManager)
level5 = Level5(screen, clock, events, sceneManager)

#scene1 = Scene1(sceneManager)
#scene2 = Scene2(sceneManager)
#scene3 = Scene3(sceneManager)

scenes = {'splashScreen': splashScreen, 'mainMenu': mainMenu, 'level1': level1, 'level2': level2, 'level3': level3, 'level4': level4, 'level5': level5}

async def main():
    while True:
        EventCheck(events)
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