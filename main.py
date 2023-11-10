import pygame
import time
import sys

from player import Player
from utilities import *

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

class Object(pygame.sprite.Sprite):
    def __init__(self, tile, pos, cost):
        self.tile = tile
        self.pos = pos
        self.cost = cost

        super().__init__()

    def ValidateTile():
        pass

class PointObj(Object):
    def __init__(self, position):
        tile = 42
        pos = 40
        cost = 1
        
        super().__init__(tile, pos, cost)

        self.image = pygame.image.load('Sprites/Objects/point.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

class PointHandler():
    def __init__(self, playMode):
        
        self.playMode = playMode
        self.pointList = []

    def AddPoint(self, position):
        point = PointObj(position)
        self.pointList.append(point)

    def DeletePoint(self,index):
        self.pointList.pop(index)

    def DrawPoints(self, screen, playerRect):
        if self.pointList:
            currentPoint = self.pointList[0]
            pygame.draw.line(screen, (255, 255, 255), playerRect.center, currentPoint.rect.center, 4)

            for a in range(len(self.pointList) - 1):
                pygame.draw.line(screen, (255, 255, 255), self.pointList[a].rect.center, self.pointList[a + 1].rect.center, 4)

        for point in self.pointList:
            screen.blit(point.image, (point.rect.x, point.rect.y))

    def Update(self, screen, playerRect, leftClick, rightClick, valid, pauseGame):

        if self.playMode == False:
            if leftClick and valid: 
                self.AddPoint(calcMouseTilePos())

            if rightClick and self.pointList:
                self.DeletePoint(len(self.pointList) - 1)

            if self.pointList:
                if playerRect.center == self.pointList[0].rect.center:
                    self.DeletePoint(0)

        self.DrawPoints(screen, playerRect)

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

        sprites = cutSpritesheet(self.tilesetSprite, 64, 64)
        tiles.extend(sprites)

        tileWidth = 64
        tileHeight = 64
        for y, row in enumerate(self.map):
            for x, tileIndex in enumerate(row):
                tilemap.blit(tiles[tileIndex], (x * tileWidth, y * tileHeight))
                if tileIndex != 0 and tileIndex != 42:
                    tileRects.append(pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
        
        self.screen.blit(tilemap, (0,0))

class Button():
    def __init__(self, text, font, fontSize, textNormalColor, textHoverColor, normalColor, hoverColor, btnSize, pos, command):
        self.text = text
        self.textNormalColor = textNormalColor
        self.textHoverColor = textHoverColor
        self.font = font
        self.fontSize = fontSize
        self.btnSize = btnSize
        self.pos = pos
        self.normalColor = normalColor
        self.hoverColor = hoverColor
        self.command = command
        self.normalSurface = self.CreateSurface(self.textNormalColor, self.normalColor)
        self.hoverSurface = self.CreateSurface(self.textHoverColor, self.hoverColor)
        self.buttonRect = pygame.Rect(self.pos, self.btnSize)
    
    def CreateSurface(self, textColor, btnColor):
        surface = pygame.Surface(self.btnSize)
        surface.fill(btnColor)
        font = pygame.font.Font(self.font, self.fontSize)
        textObj = font.render(self.text, 1, textColor)
        textRect = textObj.get_rect(center = (self.btnSize[0] / 2, self.btnSize[1] / 2))
        surface.blit(textObj, textRect)
        return surface      

    def Update(self, surface, click):

        if CheckUICollision(self.buttonRect):
            surface.blit(self.hoverSurface, self.pos)
            if click:
                self.command()

        else:
            surface.blit(self.normalSurface, self.pos)
        
class Background():
    def __init__(self, backgroundSprite, screen, speed):
        self.backgroundSprite = backgroundSprite
        self.screen = screen
        self.speed = speed
        self.offset = [0, 0]

    def DrawBackground(self):
        bgX, bgY = self.backgroundSprite.get_size()
        screenX, screenY = self.screen.get_size()

        xRepeat = screenX // bgX + 2
        yRepeat = screenY // bgY + 2

        if self.speed[0] >= 0:
            self.offset[0] += self.speed[0]
            if self.offset[0] >= bgX:
                self.offset[0] = 0

        elif self.speed[0] < 0:
            self.offset[0] += self.speed[0]
            if self.offset[0] <= -bgX:
                self.offset[0] = 0

        if self.speed[1] >= 0:
            self.offset[1] += self.speed[1]
            if self.offset[1] >= bgY:
                self.offset[1] = 0
        
        elif self.speed[1] < 0:
            self.offset[1] += self.speed[1]
            if self.offset[1] <= -bgY:
                self.offset[1] = 0


        for x in range(xRepeat):
            for y in range(yRepeat):
                screen.blit(self.backgroundSprite, ((x * bgX) + self.offset[0], (y * bgY) + self.offset[1]))

class MainMenu():
    def __init__(self, screen, clock, inputs, sceneManager):
        self.screen = screen
        self.clock = clock

        self.backgroundSprite = pygame.image.load("Sprites/UI/background.jpg")
        self.background = Background(self.backgroundSprite, screen, [-1, -1])

        self.logo = pygame.image.load("Sprites/UI/logo.png").convert_alpha()

        self.sceneManager = sceneManager

        self.inputs = inputs

        self.startButton = Button("START", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 300), self.OnStartBtnClick)
        self.settingsButton = Button("SETTINGS", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 400), sys.exit)
        self.quitButton = Button("QUIT", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 500), sys.exit)

        self.screenX, self.screenY = screen.get_size()

    def OnStartBtnClick(self):
        self.sceneManager.LoadScene('scene1')

    def Update(self):
        screen.fill((0, 0, 0))

        self.background.DrawBackground()

        self.screen.blit(self.logo, (self.screenX / 2 - 300, 50))
        #DrawText('MANIRIUS', verminVibes, 100, (255, 255, 255), screen, self.screenX / 2, 150)

        self.startButton.Update(screen, self.inputs['leftClick'])
        self.settingsButton.Update(screen, self.inputs['leftClick'])
        self.quitButton.Update(screen, self.inputs['leftClick'])

class LevelCompleteCanvas():
    def __init__(self, screen):
        self.screenX, self.screenY = screen.get_size()
        self.levelCompletePanel = pygame.Surface((self.screenX, self.screenY))
        self.levelCompletePanel.fill((0,0,0))
        self.levelCompletePanel.set_alpha(100)

        self.nextLevelBtn = Button("Next Level", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (100, 350), sys.exit)
        self.retryBtn = Button("Retry", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (390, 350), sys.exit)
        self.mainMenuBtn = Button("Main Menu", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (390, 450), sys.exit)
        self.levelSelectorBtn = Button("Level Selector", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (100, 450), sys.exit)

    def Draw(self, screen, click):
        screen.blit(self.levelCompletePanel, (0, 0))

        self.nextLevelBtn.Update(screen, click)
        self.retryBtn.Update(screen, click)
        self.mainMenuBtn.Update(screen, click)
        self.levelSelectorBtn.Update(screen, click)

        DrawText('LEVEL COMPLETE!', verminVibes, 75, (255, 255, 255), screen, self.screenX / 2, self.screenY / 3)

class UI():
    def __init__(self, player, gameManager, clock):
        self.player = player
        self.clock = clock
        self.gameManager = gameManager

        self.hud = HUD(self.player, self.gameManager)

    def Update(self):
        self.hud.Update()

class HUD():
    def __init__(self, player, gameManager):
        self.player = player
        self.gameManager = gameManager
        self.startTimer = 100

    def StartTimer(self):
        self.startTimer = time.Time()

    def DrawTime(self):
        elapsedTime = time.Time() - self.startTimer
        DrawText(str(elapsedTime), kenneyPixel, 30, (255, 255, 255), screen, 100, 100)

    def DrawSpeed(self):
        pass

    def Update(self):
        pass

class Scene():
    def __init__(self, screen, clock, playerStartPos, winPos, mapArray, inputs, sceneManager):
        self.screen = screen
        self.clock = clock

        self.clockTick = 60

        self.playerStartPos = playerStartPos
        self.winPos = winPos

        self.mapArray = mapArray

        self.playMode = False
        self.pauseGame = False
        self.complete = False
        self.itemSelected = False

        self.inputs = inputs

        self.sceneManager = sceneManager

        self.pointHandler = PointHandler(self.playMode)
        self.tileHandler = TileHandler(mapArray)
        self.player = Player(self.playerStartPos)
        self.level = Level(mapArray, "Sprites/Tileset/tileset.png", screen)

        self.hud = HUD(inputs, self.player)

        self.levelCompleteCanvas = LevelCompleteCanvas(screen)
    
        self.clockTick = 60

    def CheckProgress(self):
        if self.player.rect.x == self.winPos[0] and self.player.rect.y == self.winPos[1]:
            self.complete = True

    def SceneUpdate(self):

        self.CheckProgress()

        if self.inputs['space']:
            self.playMode = not self.playMode
            if not self.playMode:
                self.player.rect.x = self.playerStartPos[0]
                self.player.rect.y = self.playerStartPos[1]

        if self.inputs['one']:
            if not self.playMode:
                self.itemSelected = not self.itemSelected

        if self.inputs['tab']:
            self.clockTick += 30

            if self.clockTick > 120:
                self.clockTick = 60

        if self.playMode and self.itemSelected:
            self.itemSelected = False

        if not self.pointHandler.pointList:
            self.playMode = False

class Scene1(Scene):
    def __init__(self, screen, clock, inputs, sceneManager):
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

        super().__init__(screen, clock, playerStartPos, winPos, mapArray, inputs, sceneManager)

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
            self.sceneManager.LoadScene('scene2')

class Scene2(Scene):
    def __init__(self, screen, clock, inputs, sceneManager):
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

        super().__init__(screen, clock, playerStartPos, winPos, mapArray, inputs, sceneManager)

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
            self.sceneManager.LoadScene('scene3')

class Scene3(Scene):
    def __init__(self, screen, clock, inputs, sceneManager):
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

        super().__init__(screen, clock, playerStartPos, winPos, mapArray, inputs, sceneManager)

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

class TileHandler():
    def __init__(self, mapArray):
        self.possibleTiles = []
        self.mapArray = mapArray
        self.mouseTilePos = []
        self.valid = False

    def validateTile(self, mouseTilepos, tiles):
        return mouseTilepos in tiles

    def drawValidPoint(self, valid, drawPos):
        selectedTileSurface = pygame.Surface((64, 64), pygame.SRCALPHA)  # Use SRCALPHA para permitir transparência
        pointSprite = pygame.image.load('Sprites/Objects/point.png').convert_alpha()


        if not valid:
            color = (255, 0, 0, 255)
        else:
            color = (0, 255, 0, 255)

        selectedTileSurface.fill(color)
        pointSprite.blit(selectedTileSurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(pointSprite, drawPos)

    def testPossibleTiles(self, objectRect, movement):
        objectTilePos = (objectRect.x // 64, objectRect.y // 64)
        mapSizeX, mapSizeY = len(self.mapArray[0]), len(self.mapArray)

        possibleTiles = []

        if movement == "tower":
            def testTile(row, column):
                if self.mapArray[column][row] != 42:
                    return False
                return True

            for column in range(objectTilePos[0], mapSizeX):  # Da posição do objeto até o final do mapa
                if not testTile(column, objectTilePos[1]):
                    break
                possibleTiles.append(( column * 64, objectTilePos[1] * 64))

            for column in range(objectTilePos[0], 0, -1):  # Da posição do objeto até o início do mapa
                if not testTile(column, objectTilePos[1]):
                    break
                possibleTiles.append(( column * 64, objectTilePos[1] * 64))
        
            for row in range(objectTilePos[1], mapSizeY):  
                if not testTile(objectTilePos[0], row):
                    break
                possibleTiles.append((objectTilePos[0] * 64, row * 64, ))

            for row in range(objectTilePos[1], 0, -1):  
                if not testTile(objectTilePos[0], row):
                    break
                possibleTiles.append((objectTilePos[0] * 64, row * 64, ))

            return possibleTiles
        
    def drawPossibleTiles(self, tiles, screen):
            
            for tile in tiles:
                row, column = tile
                surface = pygame.Surface((64, 64))
                surface.fill((255, 255, 255))
                surface.set_alpha(75)
                screen.blit(surface, (row, column))

    def Update(self, screen, objectRect):
        self.possibleTiles = self.testPossibleTiles(objectRect, "tower") 

        self.mouseTilePos = calcMouseTilePos()
        self.valid = self.validateTile(self.mouseTilePos, self.possibleTiles)
        
        self.drawPossibleTiles(self.possibleTiles, screen)
        self.drawValidPoint(self.valid, self.mouseTilePos)

class SceneManager():
    def __init__(self, initialScene):
        self.currentScene = initialScene
    
    def LoadScene(self, scene):
        self.currentScene = scene
    
    def GetScene(self):
        return self.currentScene

#region Heliópolis

inputs = {'space': False, 'rightClick': False, 'leftClick': False, 'escape': False, 'tab': False, 'one': False}

sceneManager = SceneManager('mainMenu')

mainMenu = MainMenu(screen, clock, inputs, sceneManager)
scene1 = Scene1(screen, clock, inputs, sceneManager)
scene2 = Scene2(screen, clock, inputs, sceneManager)
scene3 = Scene3(screen, clock, inputs, sceneManager)

scenes = {'mainMenu': mainMenu, 'scene1': scene1, 'scene2': scene2, 'scene3': scene3}

while True:
    inputCheck(inputs)
    scenes[sceneManager.GetScene()].Update()
    clock.tick(60)
    pygame.display.update()

#endregion