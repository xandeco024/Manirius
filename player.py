import pygame

class Player(pygame.sprite.Sprite): #Classe do player
    def __init__(self, startPos):
        super().__init__()
        self.playerSprite = "Sprites/player.png"
        self.image = pygame.image.load(self.playerSprite).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = startPos[0]
        self.rect.y = startPos[1]
        self.playerSpeed = 2

    def DrawPlayer(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def MovePlayer(self, pointHandler):
        targetPoint = self.SearchTarget(pointHandler)
        if targetPoint is not None:
            if self.rect.x - targetPoint.rect.x > 0:
                self.rect.x -= self.playerSpeed
            
            elif self.rect.x - targetPoint.rect.x < 0:
                self.rect.x += self.playerSpeed

            elif self.rect.y - targetPoint.rect.y > 0:
                self.rect.y -= self.playerSpeed

            elif self.rect.y - targetPoint.rect.y < 0:
                self.rect.y += self.playerSpeed

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
        self.DrawPlayer(screen)