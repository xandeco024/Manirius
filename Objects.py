import pygame, sys, Utilities

class Object(pygame.sprite.Sprite):
    def __init__(self, spritesheetPath, size, pos, rotation):

        self.sprites = Utilities.CutSpritesheet(spritesheetPath, size)
        self.image = self.sprites[0]
        self.image = pygame.transform.rotate(self.image, rotation)

        self.rect = self.image.get_rect(topleft = pos)

        super().__init__()

class PointObj(Object):
    def __init__(self, pos):
        
        super().__init__('Assets/Sprites/Objects/point.png', (64,64), pos, 0)

    #banana

class DecorativeObject(Object):
    def __init__(self, spritesheetPath, size, pos, rotation):
        self.pos = pos
        super().__init__(spritesheetPath, size, pos, rotation)

    def Draw(self, surface):
        surface.blit(self.image, self.pos)    
    #banana

class Button(Object):
    def __init__(self, pos, link, gameManager):
        self.link = link
        self.gameManager = gameManager
        self.pressed = False

        super().__init__('Assets/Sprites/Objects/button.png', (64,64), pos, 0)

    def Activate():
        pass

    def Update(self):
        #verificar se o jogador está em cima do botão

        if self.gameManager.player.rect.center == self.rect.center and not self.pressed:
            self.pressed = True
            self.link.Toggle()
            self.image = self.sprites[1]
            print('buceta')

    def Draw(self, surface):
        surface.blit(self.image, self.rect)

class Laser(Object):
    def __init__(self, pos, rotation, active, gameManager):

        self.active = active
        self.gameManager = gameManager

        if self.active:
            self.Enable()

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
        if self.gameManager.player.rect.center == self.rect.center and self.active:
            print('i morreu')
            self.gameManager.player.Die()

    def Draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect)
        