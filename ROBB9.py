import pygame
from Utilities import CutSpritesheet

class Player(pygame.sprite.Sprite): #Classe do player
    def __init__(self, startPos):
        super().__init__()
        self.playerSprite = "Sprites/ROBB9/ROBB9.png"
        self.image = pygame.image.load(self.playerSprite).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = startPos[0]
        self.rect.y = startPos[1]
        self.playerSpeed = 2

        self.direction = [0,0]

        self.animationTimer = 0
        self.currentSprite = 0

        self.animations = {
            'idle': {
                'spritesheet': "Sprites/ROBB9/ROBB9.png",
                'frames': 1,
                'speed': 1,
            },
            'sliding': {
                'spritesheet': "Sprites/ROBB9/sliding sheet.png",
                'frames': 4,
                'speed': 0.1,
            },
            'dying': {
                'spritesheet': "Sprites/ROBB9/dying sheet.png",
                'frames': 4,
                'speed': 0.1,
            },
            'damage': {
                'spritesheet': "Sprites/ROBB9/damage sheet.png",
                'frames': 4,
                'speed': 0.1,
            }
        }

        self.sprites = CutSpritesheet(self.animations['idle']['spritesheet'], 64, 64)

    def Animate(self, animation):
        self.sprites = CutSpritesheet(self.animations[animation]['spritesheet'], 64, 64)

        self.currentSprite += self.animations[animation] ['speed']

        if self.currentSprite > self.animations[animation] ['frames'] - 1:
            self.currentSprite = 0
            done = True

        else:
            done = False

        self.image = self.sprites[int(self.currentSprite)]
        return done
    
    def HandleAnimations(self):
        if self.direction == [0,0]:
            self.Animate('idle')

        if self.direction != [0,0]:
            self.Animate('sliding')

    def DrawPlayer(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def MovePlayer(self, pointHandler):
        targetPoint = self.SearchTarget(pointHandler)
        if targetPoint is not None:
            if self.rect.x - targetPoint.rect.x > 0:
                self.rect.x -= self.playerSpeed
                self.direction = [-1,0]
            
            elif self.rect.x - targetPoint.rect.x < 0:
                self.rect.x += self.playerSpeed
                self.direction = [1,0]

            elif self.rect.y - targetPoint.rect.y > 0:
                self.rect.y -= self.playerSpeed
                self.direction = [0,-1]

            elif self.rect.y - targetPoint.rect.y < 0:
                self.rect.y += self.playerSpeed
                self.direction = [0,1]

        else :
            self.direction = [0,0]

    def SearchTarget(self, pointHandler):
        if pointHandler.pointList:
            return pointHandler.pointList[0]
        
        else:
            return None
        
    def Update(self, screen, pointHandler, playMode):

        if pointHandler.pointList:
            if self.rect.center == pointHandler.pointList[0].rect.center:
                pointHandler.DeletePoint(0)

        if playMode:
            self.MovePlayer(pointHandler)

        self.HandleAnimations()

        self.Rotate(self.direction)

        self.DrawPlayer(screen)
                
    def Rotate(self, dir):

        if dir == [1,0]:
            self.image = pygame.transform.rotate(self.image, 270)
        elif dir == [-1, 0]:
            self.image = pygame.transform.rotate(self.image, 90)
        elif dir == [0, 1]:
            self.image = pygame.transform.rotate(self.image, 180)
        elif dir == [0, -1]:
            self.image = pygame.transform.rotate(self.image, 0)