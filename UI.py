import pygame
import time
from Utilities import *

verminVibes = "Fonts/Vermin Vibes 1989.ttf"
kenneyPixel = "Fonts/Kenney Pixel.ttf"

class UIButton():
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

class UISpriteButton(pygame.sprite.Sprite):
    def __init__(self, screen, sprite, pos, command):

        self.screen = screen
        #self.brighten = 100

        super().__init__()
        self.sprite = pygame.image.load(sprite)
        self.pos = pos
        self.command = command
        self.rect = self.sprite.get_rect(center = self.pos)

    def DrawButton(self):
        #self.sprite.fill((self.brighten, self.brighten, self.brighten), special_flags=pygame.BLEND_RGB_ADD)
        self.screen.blit(self.sprite, self.rect)

    def Update(self, click):

        #brighten = 128

        self.DrawButton()

        if CheckUICollision(self.rect):
            if click:
                self.command()

class UI():
    def __init__(self, player, gameManager, clock, screen):
        self.player = player
        self.clock = clock
        self.screen = screen
        self.gameManager = gameManager

        self.hud = HUDCanvas(self)

    def Update(self):
        self.hud.Update()

class HUDCanvas():
    def __init__(self, ui):
        self.player = ui.player
        self.gameManager = ui.gameManager
        self.startTimer = 100

    def StartTimer(self):
        self.startTimer = time.Time()

    def DrawTime(self):
        elapsedTime = time.Time() - self.startTimer
        DrawText(str(elapsedTime), kenneyPixel, 30, (255, 255, 255), self.ui.screen, 100, 100)

    def DrawSpeed(self):
        pass

    def Update(self):
        pass

class MainMenuCanvas():
    def __init__(self, screen, inputs, sceneManager):

        self.sceneManager = sceneManager
        self.inputs = inputs
        self.screen = screen
        self.screenX, self.screenY = screen.get_size()

        self.background = Background("Sprites/UI/background.jpg", screen, [-1, -1])

        self.logo = pygame.image.load("Sprites/UI/logo.png").convert_alpha()
        self.logoRect = self.logo.get_rect()

        self.startButton = UISpriteButton(screen, "Sprites/UI/start btn.png", (self.screenX / 2, self.screenY / 2 - 50), self.OnStartBtnClick)
        self.settingsButton = UISpriteButton(screen, "Sprites/UI/settings btn.png", (self.screenX / 2, self.screenY / 2 + 75), sys.exit)
        self.quitButton = UISpriteButton(screen, "Sprites/UI/quit btn.png", (self.screenX / 2, self.screenY / 2 + 200), sys.exit)

    def OnStartBtnClick(self):
        self.sceneManager.LoadScene('scene1')

    def Update(self):
        self.background.DrawBackground()
        self.screen.blit(self.logo, (self.screenX / 2 - self.logoRect.width / 2 , 50))
        self.startButton.Update(self.inputs['leftClick'])
        self.settingsButton.Update(self.inputs['leftClick'])
        self.quitButton.Update(self.inputs['leftClick'])

class Background():
    def __init__(self, backgroundSprite, screen, speed):
        self.sprite = pygame.image.load(backgroundSprite).convert_alpha()
        self.screen = screen
        self.speed = speed
        self.offset = [0, 0]

    def DrawBackground(self):
        bgX, bgY = self.sprite.get_size()
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
                self.screen.blit(self.sprite, ((x * bgX) + self.offset[0], (y * bgY) + self.offset[1]))

class LevelCompleteCanvas():
    def __init__(self, screen):
        self.screenX, self.screenY = screen.get_size()
        self.levelCompletePanel = pygame.Surface((self.screenX, self.screenY))
        self.levelCompletePanel.fill((0,0,0))
        self.levelCompletePanel.set_alpha(100)

        self.nextLevelBtn = UIButton("Next Level", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (100, 350), sys.exit)
        self.retryBtn = UIButton("Retry", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (390, 350), sys.exit)
        self.mainMenuBtn = UIButton("Main Menu", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (390, 450), sys.exit)
        self.levelSelectorBtn = UIButton("Level Selector", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (150, 50), (100, 450), sys.exit)

    def Draw(self, screen, click):
        screen.blit(self.levelCompletePanel, (0, 0))

        self.nextLevelBtn.Update(screen, click)
        self.retryBtn.Update(screen, click)
        self.mainMenuBtn.Update(screen, click)
        self.levelSelectorBtn.Update(screen, click)

        DrawText('LEVEL COMPLETE!', verminVibes, 75, (255, 255, 255), screen, self.screenX / 2, self.screenY / 3)