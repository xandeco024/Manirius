import pygame, Utilities

class PointHandler():
    def __init__(self, mapArray, gameManager):
        
        self.gameManager = gameManager
        self.pointList = []

        #Grid Handler
        self.mapArray = mapArray
        self.tiles = []
        self.possibleTiles = []
        self.valid = False
        self.currentObjectRect = None

    def UpdateSelectedTile(self):
        self.tiles = self.gameManager.scene.level.tiles
        self.selectedTile = self.tiles[0]
        mouseX, mouseY = pygame.mouse.get_pos()
        for tile in self.tiles:
            if tile.rect.collidepoint(mouseX,mouseY):
                self.selectedTile = tile

    def ValidateTile(self, selectedTile, tiles):
        return selectedTile in tiles

    def DrawPointPreview(self, valid, selectedTile, surface):
        drawPos = (selectedTile.rect.x - 320, selectedTile.rect.y)
        selectedTileSurface = pygame.Surface((64, 64), pygame.SRCALPHA)  # Use SRCALPHA para permitir transparência
        pointSprites = Utilities.CutSpritesheet('Sprites/Objects/point.png', 64, 64)

        if not valid:
            color = (255, 0, 0, 255)
        else:
            color = (0, 255, 0, 255)

        selectedTileSurface.fill(color)
        pointSprites[0].blit(selectedTileSurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(pointSprites[0], drawPos)

    def TestPossibleTiles(self, objectRect):
        objectTilePos = (objectRect.x // 64, objectRect.y // 64)
        mapSizeX, mapSizeY = len(self.mapArray[0]), len(self.mapArray)

        possibleTiles = []

        def testTile(row, column):
            if self.mapArray[column][row] != 42:
                return False
            return True

        for column in range(objectTilePos[0], mapSizeX):  # Da posição do objeto até o final do mapa
            if not testTile(column, objectTilePos[1]):
                break
            possibleTiles.append(( column * 64, objectTilePos[1] * 64))

        for column in range(objectTilePos[0], 0, -1):  # Da posição do objeto até o início do mapa
            if not testTile(column, objectTilePos[1]):
                break
            possibleTiles.append(( column * 64, objectTilePos[1] * 64))
    
        for row in range(objectTilePos[1], mapSizeY):  
            if not testTile(objectTilePos[0], row):
                break
            possibleTiles.append((objectTilePos[0] * 64, row * 64, ))

        for row in range(objectTilePos[1], 0, -1):  
            if not testTile(objectTilePos[0], row):
                break
            possibleTiles.append((objectTilePos[0] * 64, row * 64, ))

        return possibleTiles

    def DrawPossibleTiles(self, tiles, surface):
        
        for tile in tiles:
            row, column = tile
            tileSurface = pygame.Surface((64, 64))
            tileSurface.fill((255, 255, 255))
            tileSurface.set_alpha(75)
            surface.blit(tileSurface, (row, column))

    def AddPoint(self, position):
        point = PointObj(position)
        self.pointList.append(point)
        self.gameManager.pointsPlaced += 1

    def DeletePoint(self,index):
        self.pointList.pop(index)

    def DrawPoints(self, surface):
        if self.pointList:
            currentPoint = self.pointList[0]
            pygame.draw.line(surface, (255, 255, 255), self.gameManager.player.rect.center, currentPoint.rect.center, 4)

            for a in range(len(self.pointList) - 1):
                pygame.draw.line(surface, (255, 255, 255), self.pointList[a].rect.center, self.pointList[a + 1].rect.center, 4)

        for point in self.pointList:
            surface.blit(point.image, (point.rect.x, point.rect.y))

    def Draw(self, surface):
        '''if self.gameManager.pointSelected:
            self.DrawPossibleTiles(self.possibleTiles, surface)
            self.DrawPointPreview(self.valid, self.selectedTile, surface)
            self.DrawPoints(surface)'''
        
        if self.gameManager.pointSelected:
            self.DrawPossibleTiles(self.possibleTiles, surface)

    def Update(self):
        '''if self.gameManager.pointSelected and not self.gameManager.playMode:
            self.tiles = self.gameManager.scene.level.tiles

            self.UpdateSelectedTile()
            self.valid = self.ValidateTile(self.selectedTile, self.possibleTiles)

            if  self.gameManager.inputs['leftClick'] and self.valid: 
                self.AddPoint((self.selectedTile.x - 320, self.selectedTile.y))

            if self.gameManager.inputs['rightClick'] and self.pointList:
                self.DeletePoint(len(self.pointList) - 1)'''

        if self.pointList:
            self.currentObjectRect = self.pointList[len(self.pointList) - 1].rect
            if self.gameManager.player.rect.center == self.pointList[0].rect.center:
                self.DeletePoint(0)
        else:
            self.currentObjectRect = self.gameManager.player.rect

        self.possibleTiles = self.TestPossibleTiles(self.currentObjectRect) 
        
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