import pygame, sys, Utilities

class Level():
    def __init__(self, map, tilesetSprite):

        self.map = map
        self.tilesetSprite = tilesetSprite
        self.tiles, self.tilemap = self.Create()
        self.MoveTileRects((320,0))

    def Create(self):

        tiles = []
        tileSprites = []

        tilemap = pygame.Surface((640, 640))

        tileSprites.insert(0, pygame.Surface((64,64)).convert_alpha())

        sprites = Utilities.CutSpritesheet(self.tilesetSprite, 64, 64)
        tileSprites.extend(sprites)

        for y, row in enumerate(self.map):
            for x, tileIndex in enumerate(row):
                tile = Tile((x * 64, y * 64), tileSprites[tileIndex], tileIndex)
                tilemap.blit(tile.image, tile.pos)
                tiles.append(tile)

        return tiles, tilemap
        
    def MoveTileRects(self,movement):
        for tile in self.tiles:
            tile.rect = tile.rect.move(movement)

    def Draw(self, surface):
        surface.blit(self.tilemap, (0,0))

class Tile:
    def __init__(self, pos, image, tileIndex):
        self.pos = pos
        self.image = image
        self.tileIndex = tileIndex
        self.rect = self.image.get_rect(topleft = self.pos)
        self.translatedRect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)