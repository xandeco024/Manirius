import pygame
from Utilities import CutSpritesheet

class Player(pygame.sprite.Sprite): #Classe do player
    def __init__(self, startPos, pointHandler):

        super().__init__()

        self.pointHandler = pointHandler
        self.startPos = startPos
        self.playerSprite = "Sprites/ROBB9/ROBB9.png"
        self.image = pygame.image.load(self.playerSprite).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.startPos[0]
        self.rect.y = self.startPos[1]
        self.playerSpeed = 4
        self.canMove = False

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

    def MovePlayer(self):
        targetPoint = self.SearchTarget()
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

    def SearchTarget(self):
        if self.pointHandler.pointList:
            return self.pointHandler.pointList[0]
        
        else:
            return None
        
    def Update(self):

        if self.canMove:
            self.MovePlayer()

        self.HandleAnimations()

        self.Rotate(self.direction)

    def Draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def Rotate(self, dir):

        if dir == [1,0]:
            self.image = pygame.transform.rotate(self.image, 270)
        elif dir == [-1, 0]:
            self.image = pygame.transform.rotate(self.image, 90)
        elif dir == [0, 1]:
            self.image = pygame.transform.rotate(self.image, 180)
        elif dir == [0, -1]:
            self.image = pygame.transform.rotate(self.image, 0)

    def ReturnToStart(self):
        self.rect.x = self.startPos[0]
        self.rect.y = self.startPos[1]
        self.direction = [0,0]