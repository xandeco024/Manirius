import pygame, Utilities

class Player(pygame.sprite.Sprite): #Classe do player
    def __init__(self, startPos):

        super().__init__()

        self.gameManager = None
        self.pointHandler = None

        self.startPos = startPos

        self.playerSprite = "Assets/Sprites/ROBB9/ROBB9.png"
        self.image = pygame.image.load(self.playerSprite).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = self.startPos[0]
        self.rect.y = self.startPos[1]

        self.playerSpeed = 4
        self.canMove = False

        self.direction = [0,0]
        self.rotation = 0

        self.animations = {
            'idle': {
                'spritesheet': "Assets/Sprites/ROBB9/ROBB9.png",
                'size': (64, 64),
                'speed': 1,
            },
            'sliding': {
                'spritesheet': "Assets/Sprites/ROBB9/sliding sheet.png",
                'size': (64, 64),
                'speed': 0.1,
            },
            'dying': {
                'spritesheet': "Assets/Sprites/ROBB9/dying sheet.png",
                'size': (64, 64),
                'speed': 0.1,
            },
            'damage': {
                'spritesheet': "Assets/Sprites/ROBB9/damage sheet.png",
                'size': (64, 64),
                'speed': 0.1,
            }
        }

        self.animator = Utilities.Animator(self.animations)
        self.animator.SetAnimation('sliding')

    def HandleAnimations(self):
        if self.direction == [0,0]:
            self.animator.SetAnimation('sliding')

        if self.direction != [0,0]:
            self.animator.SetAnimation('sliding')

    def MovePlayer(self):
        targetPoint = self.SearchTarget()
        if targetPoint is not None:
            if self.rect.x - targetPoint.rect.x > 0:
                self.rect.x -= self.playerSpeed
                self.direction = [-1,0]
                if self.rotation != 90:
                    self.rotation = 90
            
            elif self.rect.x - targetPoint.rect.x < 0:
                self.rect.x += self.playerSpeed
                self.direction = [1,0]
                if self.rotation != 270:
                    self.rotation = 270

            elif self.rect.y - targetPoint.rect.y > 0:
                self.rect.y -= self.playerSpeed
                self.direction = [0,-1]
                if self.rotation != 0:
                    self.rotation = 0

            elif self.rect.y - targetPoint.rect.y < 0:
                self.rect.y += self.playerSpeed
                self.direction = [0,1]
                if self.rotation != 180:
                    self.rotation = 180

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

        self.animator.Update()
        #self.HandleAnimations()

    def Draw(self, surface):
        self.image, self.done = self.animator.GetAnimation()
        self.image = pygame.transform.rotate(self.image, self.rotation)
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def ReturnToStart(self):
        self.rect.x = self.startPos[0]
        self.rect.y = self.startPos[1]
        self.direction = [0,0]