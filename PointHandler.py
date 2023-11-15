import pygame, Utilities

class PointHandler():
    def __init__(self, gameManager):
        
        self.gameManager = gameManager
        self.pointList = []

    def AddPoint(self, position):
        point = PointObj(position)
        self.pointList.append(point)
        self.gameManager.pointsPlaced += 1

    def DeletePoint(self,index):
        self.pointList.pop(index)

    def DrawPoints(self):
        if self.pointList:
            currentPoint = self.pointList[0]
            pygame.draw.line(self.gameManager.screen, (255, 255, 255), self.gameManager.player.rect.center, currentPoint.rect.center, 4)

            for a in range(len(self.pointList) - 1):
                pygame.draw.line(self.gameManager.screen, (255, 255, 255), self.pointList[a].rect.center, self.pointList[a + 1].rect.center, 4)

        for point in self.pointList:
            self.gameManager.screen.blit(point.image, (point.rect.x, point.rect.y))

    def Update(self, valid):

        if not self.gameManager.playMode and self.gameManager.pointSelected:
            if  self.gameManager.inputs['leftClick'] and valid: 
                self.AddPoint(Utilities.CalcMouseTilePos())

            if self.gameManager.inputs['rightClick'] and self.pointList:
                self.DeletePoint(len(self.pointList) - 1)

            if self.pointList:
                if self.gameManager.player.rect.center == self.pointList[0].rect.center:
                    self.DeletePoint(0)

        self.DrawPoints()

        
class Object(pygame.sprite.Sprite):
    def __init__(self, tile, pos, cost):
        self.tile = tile
        self.pos = pos
        self.cost = cost

        super().__init__()

    def ValidateTile():
        pass

class PointObj(Object):
    def __init__(self, position):
        tile = 42
        pos = 40
        cost = 1
        
        super().__init__(tile, pos, cost)

        self.image = pygame.image.load('Sprites/Objects/point.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]