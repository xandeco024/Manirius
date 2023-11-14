import pygame, time, Utilities, sys

verminVibes = "Fonts/Vermin Vibes 1989.ttf"
kenneyPixel = "Fonts/Kenney Pixel.ttf"

def DrawText(text, font, fontSize, color, surface, x, y):
    fontObj = pygame.font.Font(font, fontSize)
    textObj = fontObj.render(text, 1, color)

    lines = text.splitlines()  # divide o texto em linhas
    for i, line in enumerate(lines):
        textObj = fontObj.render(line, 1, color)
        textRect = textObj.get_rect()
        textRect.center = (x, y + i*fontSize)  # ajusta a posição y para cada linha
        surface.blit(textObj, textRect)

def CheckUICollision(rect):
    mouseX, mouseY = pygame.mouse.get_pos()
    if rect.collidepoint(mouseX, mouseY):
        return True
    else:
        return False

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

        if Utilities.CheckUICollision(self.buttonRect):
            surface.blit(self.hoverSurface, self.pos)
            if click:
                self.command()

        else:
            surface.blit(self.normalSurface, self.pos)

class UISpriteButton(pygame.sprite.Sprite):
    def __init__(self, sprite, pos, command):

        #self.brighten = 100

        super().__init__()
        self.sprite = sprite
        self.pos = pos
        self.command = command
        self.rect = self.sprite.get_rect(center = self.pos)

    def DrawButton(self, surface):
        #self.sprite.fill((self.brighten, self.brighten, self.brighten), special_flags=pygame.BLEND_RGB_ADD)
        surface.blit(self.sprite, self.rect)

    def Update(self, click):

        if CheckUICollision(self.rect):
            if click:
                self.command()

class UIImage(pygame.sprite.Sprite):
    def __init__(self, sprite, pos):
        super().__init__()
        self.sprite = sprite
        self.pos = pos
        self.rect = self.sprite.get_rect(center = self.pos)

    def DrawImage(self, surface):
        surface.blit(self.sprite, self.rect)

    def Update(self):
        pass

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
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.startTimer = 100

        self.screenX, self.screenY = gameManager.screen.get_size()
        self.hudSurface = pygame.Surface((self.screenX, self.screenY))
        self.hudSurface.set_colorkey((0, 0, 0))

        #Control

        self.playButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/play btn.png', 64, 64)
        self.playButton = UISpriteButton(self.playButtonSprites[0], (320, 32), self.gameManager.TogglePlayMode)

        self.speedButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/speed btn.png', 64, 64)
        self.speedButton1 = UISpriteButton(self.speedButtonSprites[0], (32, 32), self.OnSpeed1Clicked)
        self.speedButton2 = UISpriteButton(self.speedButtonSprites[3], (32+64, 32), self.OnSpeed2Clicked)
        self.speedButton3 = UISpriteButton(self.speedButtonSprites[5], (32+128, 32), self.OnSpeed3Clicked)

        self.creatorButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/creator btn.png', 128, 128)
        self.creatorButton = UISpriteButton(self.creatorButtonSprites[1], (576, 576), self.gameManager.TogglePlayMode)

    def StartTimer(self):
        self.startTimer = time.Time()

    def DrawTime(self):
        elapsedTime = time.Time() - self.startTimer
        Utilities.DrawText(str(elapsedTime), kenneyPixel, 30, (255, 255, 255), self.ui.screen, 100, 100)

    def DrawPointsPlaced(self):
        #DrawText(str(self.gameManager.pointHandler.pointsPlaced), kenneyPixel, 30, (255, 255, 255), surface, 50, 50)
        pass

    def DrawSpeed(self):
        pass

    def SceneControl(self):
        pass

    def DrawHUD(self):
        self.hudSurface.fill((0, 0, 0))
        self.playButton.DrawButton(self.hudSurface)

        self.speedButton1.DrawButton(self.hudSurface)
        self.speedButton2.DrawButton(self.hudSurface)
        self.speedButton3.DrawButton(self.hudSurface)

        self.creatorButton.DrawButton(self.hudSurface)

        self.gameManager.screen.blit(self.hudSurface, (0, 0))

    def Update(self):
        if self.gameManager.playMode:
            self.playButton.sprite = self.playButtonSprites[1]
        else:
            self.playButton.sprite = self.playButtonSprites[0]

        self.playButton.Update(self.gameManager.inputs['leftClick'])
        self.speedButton1.Update(self.gameManager.inputs['leftClick'])
        self.speedButton2.Update(self.gameManager.inputs['leftClick'])
        self.speedButton3.Update(self.gameManager.inputs['leftClick'])

    def HandleSpeedButtons(self):
        if self.gameManager.inputs['tab']:
            pass

    def OnSpeed1Clicked(self):
        self.gameManager.SimulationSpeed1()
        self.speedButton1.sprite = self.speedButtonSprites[0]
        self.speedButton2.sprite = self.speedButtonSprites[3]
        self.speedButton3.sprite = self.speedButtonSprites[5]

    def OnSpeed2Clicked(self):
        self.gameManager.SimulationSpeed2()
        self.speedButton1.sprite = self.speedButtonSprites[1]
        self.speedButton2.sprite = self.speedButtonSprites[2]
        self.speedButton3.sprite = self.speedButtonSprites[5]

    def OnSpeed3Clicked(self):
        self.gameManager.SimulationSpeed3()
        self.speedButton1.sprite = self.speedButtonSprites[1]
        self.speedButton2.sprite = self.speedButtonSprites[3]
        self.speedButton3.sprite = self.speedButtonSprites[4]

class MainMenuCanvas():
    def __init__(self, screen, inputs, sceneManager):

        self.screen = screen
        self.screenX, self.screenY = screen.get_size()

        self.menuSurface = pygame.Surface((self.screenX, self.screenY))
        self.menuSurface.set_colorkey((0, 0, 0))

        self.sceneManager = sceneManager
        self.inputs = inputs

        self.background = Background("Sprites/UI/background.jpg", [-1, -1])

        self.logoSprite = pygame.image.load("Sprites/UI/logo.png").convert_alpha()
        self.logoImage = UIImage(self.logoSprite, (self.screenX / 2, 100))

        self.startButtonSprites = Utilities.CutSpritesheet('Sprites/UI/start btn.png', 219, 102)
        self.startButton = UISpriteButton(self.startButtonSprites[0], (self.screenX / 2, self.screenY / 2 - 50), self.OnStartBtnClick)
        
        self.settingsButtonSprites = Utilities.CutSpritesheet('Sprites/UI/settings btn.png', 219, 102)
        self.settingsButton = UISpriteButton(self.settingsButtonSprites[0], (self.screenX / 2, self.screenY / 2 + 75), sys.exit)
        
        self.quitButtonSprites = Utilities.CutSpritesheet('Sprites/UI/quit btn.png', 219, 102)
        self.quitButton = UISpriteButton(self.quitButtonSprites[0], (self.screenX / 2, self.screenY / 2 + 200), sys.exit)

    def OnStartBtnClick(self):
        self.sceneManager.LoadScene('scene1')

    def DrawMenu(self):
        self.menuSurface.fill((0, 0, 0))

        self.background.DrawBackground(self.menuSurface)

        self.logoImage.DrawImage(self.menuSurface)

        self.startButton.DrawButton(self.menuSurface)
        self.settingsButton.DrawButton(self.menuSurface)
        self.quitButton.DrawButton(self.menuSurface)

        self.screen.blit(self.menuSurface, (0, 0))

    def Update(self):
        self.startButton.Update(self.inputs['leftClick'])
        self.settingsButton.Update(self.inputs['leftClick'])
        self.quitButton.Update(self.inputs['leftClick'])

        self.DrawMenu()

class Background():
    def __init__(self, backgroundSprite, speed):
        self.sprite = pygame.image.load(backgroundSprite).convert_alpha()
        self.speed = speed
        self.offset = [0, 0]

    def DrawBackground(self, surface):
        bgX, bgY = self.sprite.get_size()
        screenX, screenY = surface.get_size()

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
                surface.blit(self.sprite, ((x * bgX) + self.offset[0], (y * bgY) + self.offset[1]))

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

        Utilities.DrawText('LEVEL COMPLETE!', verminVibes, 75, (255, 255, 255), screen, self.screenX / 2, self.screenY / 3)