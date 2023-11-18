import pygame, time, Utilities, sys

verminVibes = "Fonts/Vermin Vibes 1989.ttf"
kenneyPixel = "Fonts/Kenney Pixel.ttf"

def DrawText(text, font, fontSize, color, surface, pos):
    fontObj = pygame.font.Font(font, fontSize)
    textObj = fontObj.render(text, 1, color)

    lines = text.splitlines()  # divide o texto em linhas
    for i, line in enumerate(lines):
        textObj = fontObj.render(line, 1, color)
        textRect = textObj.get_rect()
        textRect.center = (pos[0], pos[1] + i*fontSize)  # ajusta a posição y para cada linha
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
    def __init__(self, sprite, pos, clickCommand, hoverCommand):

        #self.brighten = 100

        super().__init__()
        self.sprite = sprite
        self.pos = pos
        self.clickCommand = clickCommand
        self.hoverCommand = hoverCommand
        self.rect = self.sprite.get_rect(topleft = pos)

        self.isHovered = False

    def DrawButton(self, surface):
        surface.blit(self.sprite, self.pos)

    def Update(self, click):

        if CheckUICollision(self.rect):
            if self.isHovered == False:
                self.isHovered = True
                self.hoverCommand()
            if click:
                self.clickCommand()

        else:
            self.isHovered = False

class UIImage(pygame.sprite.Sprite):
    def __init__(self, sprite, pos):
        super().__init__()
        self.sprite = sprite
        self.pos = pos
        self.rect = self.sprite.get_rect(topleft = pos)

    def DrawImage(self, surface):
        surface.blit(self.sprite, self.pos)

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
        self.hudSurface.set_colorkey((0, 255, 0))

        self.hoverSFX = pygame.mixer.Sound('SFX/UI/select.ogg')
        self.clickSFX = pygame.mixer.Sound('SFX/UI/click.ogg')

        #Control

        self.playButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/play btn.png', (64, 64))
        self.playButton = UISpriteButton(self.playButtonSprites[0], (self.screenX / 2 - 32, self.screenY - 64), self.OnPlayButtonClicked, self.OnPlayButtonHover)

        self.restartButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/restart btn.png', (64, 64))
        self.restartButton = UISpriteButton(self.restartButtonSprites[0], (self.screenX / 2 + 32, self.screenY - 64), self.OnRestartButtonClicked, self.OnRestartButtonHover)

        self.pauseButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/pause btn.png', (64, 64))
        self.pauseButton = UISpriteButton(self.pauseButtonSprites[0], (self.screenX / 2 - 96, self.screenY - 64), self.OnPauseButtonClicked, self.OnPauseButtonHover)

        self.speedButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/speed btn.png', (64, 64))
        self.speedUpButton = UISpriteButton(self.speedButtonSprites[2], (256, self.screenY - 64), self.OnSpeedUpClicked, self.OnSpeedUpHover)
        self.speedDownButton = UISpriteButton(self.speedButtonSprites[0], (128, self.screenY - 64), self.OnSpeedDownClicked, self.OnSpeedDownHover)

        self.creatorButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/creator btn.png', (128, 128))
        self.creatorButton = UISpriteButton(self.creatorButtonSprites[1], (self.screenX - 4*64, self.screenY - 2*64), self.OnCreatorButtonClicked, self.OnCreatorButtonHover)

        self.pointHudButtonSprites = Utilities.CutSpritesheet('Sprites/UI/HUD/point btn.png', (64, 64))
        self.pointHudButton = UISpriteButton(self.pointHudButtonSprites[0], (self.screenX - 7*64, self.screenY - 64), self.OnPointHudButtonClicked, self.OnPointHudButtonHover)

        self.hudPanel = UIImage(pygame.image.load('Sprites/UI/HUD/hud panel.png').convert_alpha(), (0, self.screenY - 128))

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

    def DrawHUD(self, surface):
        self.hudSurface.fill((0, 255, 0))

        self.hudPanel.DrawImage(self.hudSurface)
        self.playButton.DrawButton(self.hudSurface)
        self.pauseButton.DrawButton(self.hudSurface)
        self.restartButton.DrawButton(self.hudSurface)


        self.speedUpButton.DrawButton(self.hudSurface)
        self.speedDownButton.DrawButton(self.hudSurface) 

        self.pointHudButton.DrawButton(self.hudSurface)
        self.creatorButton.DrawButton(self.hudSurface)

        DrawText(str(self.gameManager.speed) + 'x', kenneyPixel, 64, (255, 255, 255), self.hudSurface, (224, self.screenY - 32))

        surface.blit(self.hudSurface, (0, 0))

    def Update(self):
        if self.gameManager.playMode:
            self.playButton.sprite = self.playButtonSprites[1]
        else:
            self.playButton.sprite = self.playButtonSprites[0]

        if self.gameManager.speed == 1:
            self.speedDownButton.sprite = self.speedButtonSprites[1]
            self.speedUpButton.sprite = self.speedButtonSprites[2]

        elif self.gameManager.speed == 2:
            self.speedDownButton.sprite = self.speedButtonSprites[0]
            self.speedUpButton.sprite = self.speedButtonSprites[2]

        elif self.gameManager.speed == 3:
            self.speedDownButton.sprite = self.speedButtonSprites[0]
            self.speedUpButton.sprite = self.speedButtonSprites[3]

        self.playButton.Update(self.gameManager.inputs['leftClick'])
        self.speedUpButton.Update(self.gameManager.inputs['leftClick'])
        self.speedDownButton.Update(self.gameManager.inputs['leftClick'])
        self.pauseButton.Update(self.gameManager.inputs['leftClick'])
        self.restartButton.Update(self.gameManager.inputs['leftClick'])
        self.pointHudButton.Update(self.gameManager.inputs['leftClick'])
        self.creatorButton.Update(self.gameManager.inputs['leftClick'])

    def OnSpeedUpHover(self):
        #self.hoverSFX.play()
        pass

    def OnSpeedUpClicked(self):
        self.gameManager.SimulationSpeedUp()

    def OnSpeedDownHover(self):
        #self.hoverSFX.play()
        pass

    def OnSpeedDownClicked(self):
        self.gameManager.SimulationSpeedDown()

    def OnPauseButtonHover(self):
        #self.hoverSFX.play()
        pass

    def OnPauseButtonClicked(self):
        pass

    def OnPlayButtonHover(self):
        #self.hoverSFX.play()
        pass

    def OnPlayButtonClicked(self):
        self.gameManager.TogglePlayMode()

    def OnRestartButtonHover(self):
        #self.hoverSFX.play()
        pass

    def OnRestartButtonClicked(self):
        self.gameManager.RestartLevel()

    def OnCreatorButtonHover(self):
        #self.hoverSFX.play()
        pass

    def OnCreatorButtonClicked(self):
        pass

    def OnPointHudButtonHover(self):
        #self.hoverSFX.play()
        pass

    def OnPointHudButtonClicked(self):
        self.gameManager.TogglePointSelected()

class MainMenuCanvas():
    def __init__(self, surface, inputs, sceneManager):

        self.selectSFX = pygame.mixer.Sound('SFX/UI/select.ogg')
        self.clickSFX = pygame.mixer.Sound('SFX/UI/click.ogg')

        self.surface = surface
        self.surfaceX, self.surfaceY = surface.get_size()

        self.menuSurface = pygame.Surface((self.surfaceX, self.surfaceY))
        self.menuSurface.set_colorkey((0, 0, 0))

        self.sceneManager = sceneManager
        self.inputs = inputs

        self.background = Background("Sprites/UI/background.jpg", [-1, -1])

        self.logoSprite = pygame.image.load("Sprites/UI/logo.png").convert_alpha()
        self.logoImage = UIImage(self.logoSprite, (self.surfaceX / 2 - 260, 100))

        self.startButtonSprites = Utilities.CutSpritesheet('Sprites/UI/start btn.png', (256, 128))
        self.startButton = UISpriteButton(self.startButtonSprites[0], (self.surfaceX / 2 - 128, self.surfaceY / 2 - 50), self.OnStartButtonClick, self.OnStartButtonHover)
        
        self.settingsButtonSprites = Utilities.CutSpritesheet('Sprites/UI/settings btn.png', (256, 128))
        self.settingsButton = UISpriteButton(self.settingsButtonSprites[0], (self.surfaceX / 2 - 128, self.surfaceY / 2 + 75), self.OnSettingsButtonClick, self.OnSettingsButtonHover)
        
        self.quitButtonSprites = Utilities.CutSpritesheet('Sprites/UI/quit btn.png', (256, 128))
        self.quitButton = UISpriteButton(self.quitButtonSprites[0], (self.surfaceX / 2 - 128, self.surfaceY / 2 + 200), self.OnQuitButtonClick, self.OnQuitButtonHover)

    def OnStartButtonHover(self):
        self.selectSFX.play()

    def OnStartButtonClick(self):
        self.clickSFX.play()
        self.sceneManager.LoadScene('scene1')

    def OnSettingsButtonHover(self):
        pass

    def OnSettingsButtonClick(self):
        pass

    def OnQuitButtonHover(self):
        pass

    def OnQuitButtonClick(self):
        sys.exit()

    def DrawMenu(self):
        self.menuSurface.fill((0, 0, 0))

        self.background.DrawBackground(self.menuSurface)

        self.logoImage.DrawImage(self.menuSurface)

        self.startButton.DrawButton(self.menuSurface)
        self.settingsButton.DrawButton(self.menuSurface)
        self.quitButton.DrawButton(self.menuSurface)

        self.surface.blit(self.menuSurface, (0, 0))

    def Update(self):
        self.startButton.Update(self.inputs['leftClick'])
        self.settingsButton.Update(self.inputs['leftClick'])
        self.quitButton.Update(self.inputs['leftClick'])

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


#region Splash
class SplashScreenCanvas1():
    pass

class SplashScreenCanvas2():
    pass

class SplashScreenCanvas3():
    pass
#endregion