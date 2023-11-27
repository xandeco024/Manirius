import pygame, sys, Utilities

class Object(pygame.sprite.Sprite):
    def __init__(self, spritesheetPath, size, pos, rotation):

        self.size = size
        self.pos = pos
        self.sprites = Utilities.CutSpritesheet(spritesheetPath, size)
        self.image = self.sprites[0]
        self.image = pygame.transform.rotate(self.image, rotation)

        self.rect = self.image.get_rect(topleft = pos)

        super().__init__()

class PointObj(Object):
    def __init__(self, pos):
        
        super().__init__('Assets/Sprites/Objects/point.png', (64,64), pos, 0)

class DecorativeObject(Object):
    def __init__(self, spritesheetPath, size, pos, rotation):
        self.pos = pos
        super().__init__(spritesheetPath, size, pos, rotation)

    def Draw(self, surface):
        if self.image is None:
            self.image = pygame.surface.Surface(self.size) 
            self.image.fill((0,0,0))
        else:
            surface.blit(self.image, self.pos)

class Button(Object):
    def __init__(self, pos, link, gameManager):
        self.link = link
        self.gameManager = gameManager
        self.pressed = False

        self.buttonSFX = pygame.mixer.Sound('Assets/SFX/Objects/SFX-Button.ogg')

        super().__init__('Assets/Sprites/Objects/button.png', (64,64), pos, 0)

    def Activate():
        pass

    def Update(self):
        #verificar se o jogador está em cima do botão

        if self.gameManager.player.rect.center == self.rect.center and not self.pressed:
            self.pressed = True
            self.buttonSFX.play()
            for obj in self.link:
                obj.Toggle()

    def Draw(self, surface):
        if self.pressed:
            self.image = self.sprites[1]
        else:
            self.image = self.sprites[0]

        surface.blit(self.image, self.rect)

class Laser(Object):
    def __init__(self, pos, rotation, initiallyActive, gameManager):

        self.rotation = rotation
        self.initiallyActive = initiallyActive
        self.gameManager = gameManager

        if self.initiallyActive:
            self.Enable()

        self.animator = Utilities.Animator({
            'standard': {
                'name': 'standard', #Nome da animação
                'spritesheet': "Assets/Sprites/Objects/laser.png",
                'size': (64, 64),
                'speed': 0.1,
            }
        })

        self.animator.SetAnimation('standard')

        super().__init__('Assets/Sprites/Objects/laser.png', (64,64), pos, rotation)

    def Enable(self):
        self.active = True

    def Disable(self):
        self.active = False

    def Toggle(self):
        if self.active:
            self.Disable()
        else:
            self.Enable()

    def Update(self):
        self.animator.Update()
        if self.gameManager.player.rect.center == self.rect.center and self.active:
            self.gameManager.player.Die()

    def Draw(self, surface):
        if self.active:
            laserImg = self.animator.GetSprite()
            laserImg = pygame.transform.rotate(laserImg, self.rotation)
            surface.blit(laserImg, self.rect)

class Portal(Object):
    def __init__(self, color, pos, link, exit, gameManager):
        self.color = color
        self.gameManager = gameManager
        self.link = link
        self.exit = exit

        self.portalSFX = pygame.mixer.Sound('Assets/SFX/Objects/SFX-Portal.ogg')

        self.animation = {
            'standard': {
                'name': 'standard', #Nome da animação
                'spritesheet': "Assets/Sprites/Objects/portal.png",
                'size': (64, 64),
                'speed': 0.2,
            }
        }

        self.animator = Utilities.Animator(self.animation)
        self.animator.SetAnimation('standard')
        self.animator.ResumeAnimation()
        super().__init__('Assets/Sprites/Objects/portal frame.png', (64,64), pos, 0)

    def Update(self):
        self.animator.Update()
        if self.gameManager.player.rect.center == self.rect.center:
            #pausa o jogo, apaga a pointlist e vai pra saida do link.
            self.gameManager.player.canMove = False
            self.gameManager.playMode = False
            self.gameManager.pointHandler.pointList.clear()
            self.gameManager.player.rect.x = self.link.exit[0]
            self.gameManager.player.rect.y = self.link.exit[1]
            self.portalSFX.play()
    

    def Draw(self, surface):
        portalImg = self.animator.GetSprite().copy()
        portalImg.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)
        self.image.blit(portalImg, (0,0))
        surface.blit(self.image, self.rect)

class Spike(Object):
    def __init__(self, pos, initiallyActive, gameManager):

        self.initiallyActive = initiallyActive
        self.gameManager = gameManager
        self.active = initiallyActive
        self.lastTurn = 0

        self.spikeEnterSFX = pygame.mixer.Sound('Assets/SFX/Objects/SFX-SpikeEnter.ogg')
        self.spikeExitSFX = pygame.mixer.Sound('Assets/SFX/Objects/SFX-SpikeExit.ogg')

        super().__init__('Assets/Sprites/Objects/spike.png', (64,64), pos, 0)

        if self.initiallyActive:
            self.image = self.sprites[1]

    def Toggle(self):
        if self.active:
            self.active = False
            self.image = self.sprites[0]
            self.spikeExitSFX.play()
        else:
            self.active = True
            self.image = self.sprites[1]
            self.spikeEnterSFX.play()

    def Update(self):

        if self.gameManager.runTimes != self.lastTurn:
            self.lastTurn = self.gameManager.runTimes
            self.Toggle()

        if self.gameManager.events['space']:
            self.Toggle()

        if self.gameManager.player.rect.center == self.rect.center and self.active:
            self.gameManager.player.Die()

    def Draw(self, surface):
        surface.blit(self.image, self.rect)