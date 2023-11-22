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

