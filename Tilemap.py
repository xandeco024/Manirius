import pygame, sys, Utilities

class Level():
    def __init__(self, map, tilesetSprite):

        super().__init__()
        self.map = map
        self.tilesetSprite = tilesetSprite

    def DrawLevel(self, surface):

        tileRects = []
        tiles = []

        tilemap = pygame.Surface((640, 640))

        tiles.insert(0, pygame.Surface((64,64)).convert_alpha())

        sprites = Utilities.CutSpritesheet(self.tilesetSprite, 64, 64)
        tiles.extend(sprites)

        tileWidth = 64
        tileHeight = 64
        for y, row in enumerate(self.map):
            for x, tileIndex in enumerate(row):
                tilemap.blit(tiles[tileIndex], (x * tileWidth, y * tileHeight))
                if tileIndex != 0 and tileIndex != 42:
                    tileRects.append(pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
        
        surface.blit(tilemap, (0,0))