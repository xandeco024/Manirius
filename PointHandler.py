import pygame, Utilities, Objects

class PointHandler():
    def __init__(self, mapArray):
        
        self.gameManager = None
        self.pointList = []

        #Grid Handler
        self.mapArray = mapArray
        self.possibleTilesPos = []
        self.valid = False
        self.currentObjectRect = None

        self.addPointSFX = pygame.mixer.Sound('Assets/SFX/Objects/SFX-AddPoint.ogg')
        self.deletePointSFX = pygame.mixer.Sound('Assets/SFX/Objects/SFX-DeletePoint.ogg')

    def CalcMouseTilePos(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX -= 320

        mouseTilePos = [mouseX // 64, mouseY // 64]

        if mouseTilePos[0] < 1:
            mouseTilePos[0] = 1

        if mouseTilePos[1] < 1:
            mouseTilePos[1] = 1

        if mouseTilePos[0] > 8:
            mouseTilePos[0] = 8
        
        if mouseTilePos[1] > 8:
            mouseTilePos[1] = 8

        mouseTilePos[0] *= 64
        mouseTilePos[1] *= 64

        return (mouseTilePos[0], mouseTilePos[1])
    
    def ValidateTilePos(self, selectedTilePos, possibleTilesPos):
        return selectedTilePos in possibleTilesPos

    def DrawPointPreview(self, valid, pos, surface):
        selectedTileSurface = pygame.Surface((64, 64), pygame.SRCALPHA)  # Use SRCALPHA para permitir transparência
        pointSprites = Utilities.CutSpritesheet('Assets/Sprites/Objects/point.png', (64, 64))

        if not valid:
            color = (255, 0, 0, 255)
        else:
            color = (0, 255, 0, 255)

        selectedTileSurface.fill(color)
        pointSprites[0].blit(selectedTileSurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(pointSprites[0], pos)

    def TestPossibleTilePos(self, objectRect):
        objectTilePos = (objectRect.x // 64, objectRect.y // 64)
        mapSizeX, mapSizeY = len(self.mapArray[0]), len(self.mapArray)

        self.possibleTilesPos.clear()

        def testTile(row, column):
            if self.mapArray[column][row] != 42:
                return False
            return True  

        for column in range(objectTilePos[0], mapSizeX):  # Da posição do objeto até o final do mapa
            if not testTile(column, objectTilePos[1]):
                break
            self.possibleTilesPos.append((column * 64, objectTilePos[1] * 64))

        for column in range(objectTilePos[0], 0, -1):  # Da posição do objeto até o início do mapa
            if not testTile(column, objectTilePos[1]):
                break
            self.possibleTilesPos.append((column * 64, objectTilePos[1] * 64))
    
        for row in range(objectTilePos[1], mapSizeY):  
            if not testTile(objectTilePos[0], row):
                break
            self.possibleTilesPos.append((objectTilePos[0] * 64, row * 64))

        for row in range(objectTilePos[1], 0, -1):  
            if not testTile(objectTilePos[0], row):
                break
            self.possibleTilesPos.append((objectTilePos[0] * 64, row * 64))

    def DrawPossibleTiles(self, tiles, surface):
        
        for tile in tiles:
            row, column = tile[0], tile[1]
            tileSurface = pygame.Surface((64, 64))
            tileSurface.fill((255, 255, 255))
            tileSurface.set_alpha(75)
            surface.blit(tileSurface, (row, column))

    def AddPoint(self, pos):
        point = Objects.PointObj(pos)
        self.pointList.append(point)
        self.gameManager.pointsPlaced += 1
        self.addPointSFX.play()

    def DeletePoint(self,index):
        self.pointList.pop(index)
        self.deletePointSFX.play()

    def DrawPoints(self, surface):
        if self.pointList:
            currentPoint = self.pointList[0]
            pygame.draw.line(surface, (255, 255, 255), self.gameManager.player.rect.center, currentPoint.rect.center, 4)

            for a in range(len(self.pointList) - 1):
                pygame.draw.line(surface, (255, 255, 255), self.pointList[a].rect.center, self.pointList[a + 1].rect.center, 4)

        for point in self.pointList:
            surface.blit(point.image, (point.rect.x, point.rect.y))

    def Draw(self, surface):
        if self.gameManager.pointSelected and not self.gameManager.playMode:
            self.DrawPossibleTiles(self.possibleTilesPos, surface)
            self.DrawPointPreview(self.valid, self.CalcMouseTilePos(), surface)

        self.DrawPoints(surface)

    def Update(self):

        if self.pointList:
            self.currentObjectRect = self.pointList[len(self.pointList) - 1].rect
            if self.pointList[0].rect.center == self.gameManager.player.rect.center:
                self.DeletePoint(0)
        else:
            self.currentObjectRect = self.gameManager.player.rect

        if not self.gameManager.playMode and self.gameManager.pointSelected:
            self.TestPossibleTilePos(self.currentObjectRect) 
            self.valid = self.ValidateTilePos(self.CalcMouseTilePos(), self.possibleTilesPos)

            if  self.gameManager.events['leftClick'] and self.valid: 
                self.AddPoint(self.CalcMouseTilePos())

            if self.gameManager.events['rightClick'] and self.pointList:
                self.DeletePoint(len(self.pointList) - 1)