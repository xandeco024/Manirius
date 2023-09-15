import pygame
import sys
import math

#region Inicio do codigo

pygame.init()
screen = pygame.display.set_mode((640, 640),0,32)
pygame.display.set_caption("SMAUG-2")
clock = pygame.time.Clock()

#endregion

attractiveObjects = pygame.sprite.Group()

#Sprites
playerSprite = "Sprites/player.png"

#Tileset
tileWidth = 64
tileHeight = 64
tilesetSprite = "Sprites/tileset.png"
tileset = pygame.image.load(tilesetSprite).convert_alpha()

map = [
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

#HUD
scoreText = 0
scoreTextColor = (255, 255, 255)

class AttactiveOBJ(pygame.sprite.Sprite): #Classe do objeto atraente
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Sprites/object.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Player(pygame.sprite.Sprite): #Classe do player
    def __init__(self, x, y, playerSpeed):
        super().__init__()
        self.image = pygame.image.load(playerSprite).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
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

def animate(sprites, frameDuration):
    frame = 0
    value = 0
    sprite = sprites[frame]

    if value >= frameDuration:
        frame += 1

    return sprite

def collisionTest(rect , tiles):
    hitList = []
    for tile in tiles:
        if rect.colliderect(tile):
            hitList.append(tile)
    return hitList

def move(rect, movement, tiles):
    collisionTypes = {'top': False, 'bottom': False, 'left': False, 'right': False}

    rect.x += movement[0]

    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[0] > 0:
            rect.right = tile.left
            collisionTypes['right'] = True

        elif movement[0] < 0:
            rect.left = tile.right
            collisionTypes['left'] = True

    rect.y += movement[1]
    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[1] > 0:
            rect.bottom = tile.top
            collisionTypes['bottom'] = True

        if movement[1] < 0:
            rect.top = tile.bottom
            collisionTypes['top'] = True
    return rect, collisionTypes

def inputList():
    inputList = pygame.key.get_pressed()
    return inputList

playerStartPos = (3/2 * 64, 3/2 * 64)

font = pygame.font.SysFont('Arial', 20)
player = Player(playerStartPos[0], playerStartPos[1], 1)

angle = 0

tilemap = pygame.Surface((640, 640))


#region cut tiles
tiles = []
tilesetSize = tileset.get_size()
tiles.insert(0, pygame.Surface((tileWidth,tileHeight)).convert_alpha())
spritesCortados = cutSpritesheet(tilesetSprite, 64, 64)
tiles.extend(spritesCortados)
#endregion

playerVelocity = [0,0]

#region selectTile

selectedTile = pygame.Surface((tileWidth, tileHeight))
selectedTile.fill((255, 255, 255))
selectedTile.set_alpha(100)

def calcMousePos(mapArray):
    mapXSize = len(mapArray[0])
    mapYSize = len(mapArray)

    mousePosition = pygame.mouse.get_pos()
    mouseTilePos = (0,0)


    for x in range(mapXSize):
        if mousePosition[0] >= x * 64 and mousePosition[0] <= (x + 1) * 64:
            mouseTilePos = (x, mouseTilePos[1])
            break
        
    for y in range(mapYSize):
        if mousePosition[1] >= y * 64 and mousePosition[1] <= (y + 1) * 64:
            mouseTilePos = (mouseTilePos[0], y)
            break

    return (mouseTilePos[0] * 64, mouseTilePos[1] * 64)
#endregion

#region validateTile
def validateTile(tilePos, mapArray):

    tilePos = (tilePos[0] // 64, tilePos[1] // 64)

    if mapArray[tilePos[1]] [tilePos[0]] == 42:
        if tilePos[0] * 64 + 32 == playerPos[0] or tilePos[1] * 64 + 32 == playerPos[1]:
            selectedTile.fill((0, 255, 0))

        else:
            selectedTile.fill((255, 255, 255))

    else:
        selectedTile.fill((255, 0, 0))

#endregion

#region keyboardMove
def keyboardMove():
    if(inputList()[pygame.K_w]):
        playerVelocity[1] = -player.playerSpeed
    elif(inputList()[pygame.K_s]):
        playerVelocity[1] = player.playerSpeed
    else:
        playerVelocity[1] = 0

    if(inputList()[pygame.K_a]):
        playerVelocity[0] = -player.playerSpeed
    elif(inputList()[pygame.K_d]):
        playerVelocity[0] = player.playerSpeed
    else:
        playerVelocity[0] = 0
#endregion

while True: #Game Loop
    
    screen.fill((100, 100, 100))

    #Atualizações 
    clock.tick(60)
    playerPos = player.rect.center
    mousePos = pygame.mouse.get_pos()
    selectedTilePos = calcMousePos(map)
    print(playerVelocity)
    validateTile(selectedTilePos, map)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Fecha o jogo
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Cria objeto no lugar do clique
            if not attractiveObjects:
                attractiveOBJ = AttactiveOBJ(selectedTilePos[0] + 32, selectedTilePos[1] + 32)
                attractiveObjects.add(attractiveOBJ)
                scoreText += 1

    if attractiveObjects: #move o player em direção ao objeto

        if player.rect.centerx < attractiveOBJ.rect.centerx:
            playerVelocity[0] = player.playerSpeed
            playerVelocity[1] = 0
        elif player.rect.centerx > attractiveOBJ.rect.centerx:
            playerVelocity[0] = -player.playerSpeed
            playerVelocity[1] = 0
        elif player.rect.centery < attractiveOBJ.rect.centery:
            playerVelocity[0] = 0
            playerVelocity[1] = player.playerSpeed
        elif player.rect.centery > attractiveOBJ.rect.centery:
            playerVelocity[0] = 0
            playerVelocity[1] = -player.playerSpeed
        else:
            playerVelocity[0] = 0
            playerVelocity[1] = 0

        if playerPos == attractiveOBJ.rect.center:
            attractiveObjects.remove(attractiveOBJ)

    #desenha o mapArray
    
    tileRects = []
    y = 0
    for row in map:
        x = 0
        for tileIndex in row:
            tilemap.blit(tiles[tileIndex], (x * tileWidth, y * tileHeight))
            if tileIndex != 0 and tileIndex != 42:
                
                tileRects.append(pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            x += 1
        y += 1

    #tilemap = pygame.transform.scale(tilemap, (640,640))
    screen.blit(tilemap, (0,0))

    #keyboardMove()

    playerRect, collisions = move(player.rect, playerVelocity, tileRects)


    #region Score
    scoreTextSurface = font.render(str(scoreText), True, scoreTextColor)
    scoreTextRect = scoreTextSurface.get_rect()
    scoreTextRect.center = (100, 200)
    #endregion

    if attractiveObjects:
        pygame.draw.line(screen, (255, 0, 0), playerPos, attractiveOBJ.rect.center)

    attractiveObjects.draw(screen)
    screen.blit(selectedTile, calcMousePos(map))
    playerRotatedImg = pygame.transform.rotate(player.image, angle)
    screen.blit(playerRotatedImg, (playerRect.x, playerRect.y))

    pygame.display.update() #Atualiza a tela