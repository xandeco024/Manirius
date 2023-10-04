import pygame
import sys

#region Inicio do codigo

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Mánirius")
clock = pygame.time.Clock()

#endregion

#Sprites
playerSprite = "Sprites/player.png"

#Tileset

map2 = [
    [31,22,63,22,22,22,22,22,22,33],
    [13,42,71,42,42,42,42,42,42,11],
    [13,42,71,42,71,42,42,42,42,11],
    [13,42,85,95,92,42,42,42,42,11],
    [13,42,42,42,71,42,42,42,42,11],
    [13,42,42,42,42,83,42,42,42,11],
    [13,42,42,42,42,42,42,42,42,11],
    [13,42,42,42,42,42,91,92,92,72],
    [13,42,42,42,42,42,42,42,42,43],
    [51, 2, 2, 2, 2, 2, 2, 2, 2,53]
]

map1 = [
    [31,22,22,22,22,22,22,22,33,12],
    [13,42,42,42,42,42,42,42,11,12],
    [13,42,42,42,42,42,42,42,11,12],
    [13,42,42,42,42,42,42,42,11,12],
    [13,42,42,42,61,42,42,42,11,12],
    [13,42,42,42,71,42,42,42,11,12],
    [13,42,42,42,71,42,42,42,11,12],
    [13,42,42,42,71,42,42,42,21,33],
    [13,42,42,42,71,42,42,42,42,43],
    [51, 2, 2, 2,62, 2, 2, 2, 2,53]
]

map = [
    [31,22,22,22,22,22,22,32,22,33],
    [13,42, 7,42,42,71,42,42,42,11],
    [13,42,42,42,42,71,42,42,42,11],
    [13,96,42,94,95,92,42,42,42,11],
    [13,42,42,42,42,71,42,42,42,11],
    [13,42,42,42,42,81,42,42,42,11],
    [13,42,42,42,42,44,42,42,42,11],
    [13,42,42,42,42, 1, 2, 2, 2,53],
    [13,42,42,42,42,11,12,12,12,12],
    [51, 2, 2, 2, 2,53,12,12,12,12]
]

class Object(pygame.sprite.Sprite):
    def __init__(self, tile, pos, cost):
        self.tile = tile
        self.pos = pos
        self.cost = cost

        super().__init__()

class PointObj(Object):
    def __init__(self, position):
        tile = 42
        pos = 40
        cost = 1
        
        super().__init__(tile, pos, cost)

        self.image = pygame.image.load('Sprites/point.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

class Player(pygame.sprite.Sprite): #Classe do player
    def __init__(self, x, y, playerSpeed):
        super().__init__()
        self.image = pygame.image.load(playerSprite).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.playerSpeed = playerSpeed

def cutSpritesheet(spritesheet, spriteWidth, spriteHeight):
    sheet = pygame.image.load(spritesheet).convert_alpha()
    sheetSize = sheet.get_size()

    sprites = []

    columns = sheetSize[0] // spriteWidth
    rows = sheetSize[1] // spriteHeight

    for column in range(columns):
        for row in range(rows):
            x = row * spriteWidth
            y = column * spriteHeight

            sprite = sheet.subsurface(pygame.Rect(x, y, * (spriteWidth, spriteHeight)))

            sprites.append(sprite)

    return sprites

def collisionTest(rect , tiles):
    hitList = []
    for tile in tiles:
        if rect.colliderect(tile):
            hitList.append(tile)
    return hitList

def move(rect, movement, tiles):
    #collisionTypes = {'top': False, 'bottom': False, 'left': False, 'right': False}

    rect.x += movement[0] #MOVIMENTO HORIZONTAL

    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[0] > 0:
            rect.right = tile.left #caso haja colisão na direita, seta o jogador na posição da parte da esquerda do tile que colidiu.
            #collisionTypes['right'] = True

        elif movement[0] < 0:
            rect.left = tile.right #caso haja colisão na esquerda, seta o jogador na posição da parte da direita do tile que colidiu.
            #collisionTypes['left'] = True

    rect.y += movement[1] #MOVIMENTO VERTICA

    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[1] > 0: 
            rect.bottom = tile.top #caso haja colisão na parte debaixo, seta o jogador na posição da parte de cima do tile que colidiu.
            #collisionTypes['bottom'] = True

        if movement[1] < 0:
            rect.top = tile.bottom #caso haja colisão na parte de cima, seta o jogador na posição da parte debaixo do tile que colidiu.
            #collisionTypes['top'] = True
    return rect#, collisionTypes

def calcMouseTilePos(mapArray):
    mapXSize = len(mapArray[0])
    mapYSize = len(mapArray)

    mousePosition = pygame.mouse.get_pos()

    tileX = mousePosition[0] // 64
    tileY = mousePosition[1] // 64

    if tileX >= mapXSize or tileY >= mapYSize:
        return (0,0)

    return (tileX, tileY)

def validateTile1(testPos, tilePos, tiles, movement):
    selectedTile = pygame.Surface((64, 64), pygame.SRCALPHA)
    valid = False

    tilePos = (tilePos[0] // 64, tilePos[1] // 64)

    if movement == "Tower":
        if map[tilePos[1]] [tilePos[0]] == tiles:
            if tilePos[0] * 64 == testPos[0] or tilePos[1] * 64 == testPos[1]:
                selectedTile.fill((0, 255, 0))
                valid = True

            else:
                selectedTile.fill((255, 255, 255))

        else:
            selectedTile.fill((255, 0, 0))
            valid = False


    return valid

def validateTile(mouseTilepos, tiles):
    return mouseTilepos in tiles

def drawValidPoint(valid, drawPos):
    selectedTileSurface = pygame.Surface((64, 64), pygame.SRCALPHA)  # Use SRCALPHA para permitir transparência
    pointSprite = pygame.image.load('Sprites/point.png').convert_alpha()


    if not valid:
        color = (255, 0, 0, 255)
    else:
        color = (0, 255, 0, 255)

    selectedTileSurface.fill(color)
    pointSprite.blit(selectedTileSurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(pointSprite, drawPos)

def testPossibleTiles(objectRect):
    objectTilePos = (objectRect[0] // 64, objectRect[1] // 64)
    mapSizeX, mapSizeY = len(map[0]), len(map)

    possibleTiles = []

    def testTile(row, column):
        if map[column][row] != 42:
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
    
def drawPossibleTiles(tiles):
        
        for tile in tiles:
            row, column = tile
            surface = pygame.Surface((64, 64))
            surface.fill((255, 255, 255))
            surface.set_alpha(75)
            screen.blit(surface, (row, column))

def drawPoints(pointList, playerRect):
    if pointList:
        currentPoint = pointList[0]
        pygame.draw.line(screen, (255, 255, 255), playerRect.center, (currentPoint.rect.centerx, currentPoint.rect.centery), 4)

        for a in range(len(pointList) - 1):
            pygame.draw.line(screen, (255, 255, 255), pointList[a].rect.center, pointList[a + 1].rect.center, 4)

    for point in pointList:
        screen.blit(point.image, (point.rect.x, point.rect.y))

class PointHandler():
    def __init__(self, pointSprite, pauseGame):

        super().__init__()
        self.pointSprite = pointSprite
        self.pauseGame = pauseGame

class Level():
    def __init__(self, map, tilesetSprite, screen):

        super().__init__()
        self.map = map
        self.tilesetSprite = tilesetSprite
        self.screen = screen

    def DrawLevel(self):

        tileRects = []
        tiles = []

        tilemap = pygame.Surface((640, 640))

        tiles.insert(0, pygame.Surface((64,64)).convert_alpha())

        sprites = cutSpritesheet(self.tilesetSprite, 64, 64)
        tiles.extend(sprites)

        tileWidth = 64
        tileHeight = 64
        for y, row in enumerate(self.map):
            for x, tileIndex in enumerate(row):
                tilemap.blit(tiles[tileIndex], (x * tileWidth, y * tileHeight))
                if tileIndex != 0 and tileIndex != 42:
                    tileRects.append(pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
        
        self.screen.blit(tilemap, (0,0))

def DrawText(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)

def MainMenu():
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DrawText('Main Menu', pygame.font.Font('freesansbold.ttf', 100), (255, 255, 255), screen, 20, 20)
        pygame.display.update()
        clock.tick(60)

def Game():
    playerVelocity = [0,0]
    pauseGame = True
    space_released = False
    itemSelected = False
    playerStartPos = (64,128)
    player = Player(playerStartPos[0], playerStartPos[1], 2)
    angle = 0
    pointList = []

    valid = False

    level = Level(map, "./Sprites/tileset.png", screen)

    while True:
        screen.fill((100, 100, 100))

        #Atualizações 
        clock.tick(60)
        playerPos = player.rect
        selectedTile = calcMouseTilePos(map)
        selectedTileTranslated = (selectedTile[0] * 64, selectedTile[1] * 64)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Fecha o jogo
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN: #Apertar tecla
                if event.key == pygame.K_0:
                    itemSelected = True

                else:
                    itemSelected = False
                
                if event.key == pygame.K_SPACE and space_released:
                    pauseGame = not pauseGame
                    space_released = False

            if event.type == pygame.KEYUP: #Soltar tecla
                if event.key == pygame.K_SPACE:
                    space_released = True

            if event.type == pygame.MOUSEBUTTONDOWN: #Botão do mouse
                
                if event.button == 1:
                    if itemSelected and valid:
                        point = PointObj(selectedTileTranslated)
                        
                        pointList.append(point)

        if pointList: #move o player em direção ao objeto

            currentPoint = pointList[0]

            dx = currentPoint.rect.x - player.rect.x
            dy = currentPoint.rect.y - player.rect.y

            if dx != 0:
                playerVelocity[0] = player.playerSpeed * (dx // abs(dx))
                playerVelocity[1] = 0
                
            elif dy != 0:
                playerVelocity[0] = 0
                playerVelocity[1] = player.playerSpeed * (dy // abs(dy))

            else:
                playerVelocity[0] = 0
                playerVelocity[1] = 0
                pointList.pop(0)

        #desenha o mapa

        tileRects = []

        if not pauseGame and pointList:
            pauseGame = True

        if not pauseGame:
            playerRect = move(player.rect, playerVelocity, tileRects)

        else:
            playerRect = player.rect

        #region Draw

        level.DrawLevel()

        if itemSelected:
            if pointList:
                valid = validateTile(selectedTileTranslated, testPossibleTiles(pointList[len(pointList) - 1].rect))
                drawPossibleTiles(testPossibleTiles(pointList[len(pointList) - 1].rect)) 
                drawValidPoint(validateTile(selectedTileTranslated, testPossibleTiles(pointList[len(pointList) - 1].rect)), selectedTileTranslated)
            else:
                valid = validateTile(selectedTileTranslated, testPossibleTiles(playerPos))
                drawPossibleTiles(testPossibleTiles(player.rect))
                drawValidPoint(validateTile(selectedTileTranslated, testPossibleTiles(playerPos)), selectedTileTranslated)

        drawPoints(pointList, playerRect)

        playerRotatedImg = pygame.transform.rotate(player.image, angle)
        screen.blit(playerRotatedImg, (playerRect.x, playerRect.y))

        pygame.display.update() #Atualiza a tela
        #endregion

#region Heliópolis
MainMenu()
#endregion