import pygame, Utilities

class GridHandler():
    def __init__(self, mapArray, gameManager):

        self.gameManager = gameManager

        self.possibleTiles = []
        self.mapArray = mapArray
        self.mouseTilePos = []
        self.valid = False

    def validateTile(self, mouseTilepos, tiles):
        return mouseTilepos in tiles

    def drawValidPoint(self, valid, drawPos):
        selectedTileSurface = pygame.Surface((64, 64), pygame.SRCALPHA)  # Use SRCALPHA para permitir transparência
        pointSprite = pygame.image.load('Sprites/Objects/point.png').convert_alpha()

        if not valid:
            color = (255, 0, 0, 255)
        else:
            color = (0, 255, 0, 255)

        selectedTileSurface.fill(color)
        pointSprite.blit(selectedTileSurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.gameManager.screen.blit(pointSprite, drawPos)

    def testPossibleTiles(self, objectRect):
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
        
    def drawPossibleTiles(self, tiles):
            
            for tile in tiles:
                row, column = tile
                surface = pygame.Surface((64, 64))
                surface.fill((255, 255, 255))
                surface.set_alpha(75)
                self.gameManager.screen.blit(surface, (row, column))

    def Update(self, objectRect):
        self.possibleTiles = self.testPossibleTiles(objectRect) 

        self.mouseTilePos = Utilities.CalcMouseTilePos()
        self.valid = self.validateTile(self.mouseTilePos, self.possibleTiles)
        
        self.drawPossibleTiles(self.possibleTiles)
        self.drawValidPoint(self.valid, self.mouseTilePos)