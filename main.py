import pygame
import sys
import math

#region Inicio do codigo

pygame.init()
screen = pygame.display.set_mode((640, 640),0,32)
pygame.display.set_caption("SMAUG-2")
clock = pygame.time.Clock()

#endregion

pointList = []

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

        self.image = pygame.image.load('Sprites/object.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

class sexoanal(pygame.sprite.Sprite): #Classe do objeto atraente
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

def collisionTest(rect , tiles):
    hitList = []
    for tile in tiles:
        if rect.colliderect(tile):
            hitList.append(tile)
    return hitList

def move(rect, movement, tiles):
    collisionTypes = {'top': False, 'bottom': False, 'left': False, 'right': False}

    rect.x += movement[0] #MOVIMENTO HORIZONTAL

    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[0] > 0:
            rect.right = tile.left #caso haja colisão na direita, seta o jogador na posição da parte da esquerda do tile que colidiu.
            collisionTypes['right'] = True

        elif movement[0] < 0:
            rect.left = tile.right #caso haja colisão na esquerda, seta o jogador na posição da parte da direita do tile que colidiu.
            collisionTypes['left'] = True

    rect.y += movement[1] #MOVIMENTO VERTICA

    hitList = collisionTest(rect, tiles)
    for tile in hitList:
        if movement[1] > 0: 
            rect.bottom = tile.top #caso haja colisão na parte debaixo, seta o jogador na posição da parte de cima do tile que colidiu.
            collisionTypes['bottom'] = True

        if movement[1] < 0:
            rect.top = tile.bottom #caso haja colisão na parte de cima, seta o jogador na posição da parte debaixo do tile que colidiu.
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

def calcMouseTilePos(mapArray):
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
def validateTile(testPos, tilePos, tiles, movement):

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

def possibleTiles(objectRect):
    objectTilePos = (objectRect[0] // 64, objectRect[1] // 64)
    mapSizeX, mapSizeY = len(map[0]), len(map)

    def draw_tile(row, column, alpha):
        if map[row][column] != 42:
            return False
        surface = pygame.Surface((64, 64))
        surface.fill((255, 255, 255))
        surface.set_alpha(alpha)
        screen.blit(surface, (column * 64, row * 64))
        return True

    # Verifica os tiles na mesma linha que o objeto
    alpha = 150
    for column in range(objectTilePos[0], mapSizeX):  # Da posição do objeto até o final do mapa
        if not draw_tile(objectTilePos[1], column, alpha):
            break
        alpha = max(0, alpha - 10)  # Reduz o valor alfa para o próximo tile

    alpha = 150  # Reinicia o valor alfa para a próxima direção
    for column in range(objectTilePos[0], -1, -1):  # Da posição do objeto até o início do mapa
        if not draw_tile(objectTilePos[1], column, alpha):
            break
        alpha = max(0, alpha - 10)  

    alpha = 150  
    for row in range(objectTilePos[1], mapSizeY):  
        if not draw_tile(row, objectTilePos[0], alpha):
            break
        alpha = max(0, alpha - 10)  

    alpha = 150  
    for row in range(objectTilePos[1], -1, -1):  
        if not draw_tile(row, objectTilePos[0], alpha):
            break
        alpha = max(0, alpha - 10)  
    
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

pauseGame = True

hotBar = [0,1,2,3,4,5,6,7,8,9]
selectedItem = hotBar[0]

def selectItem():
    if(inputList()[pygame.K_0]):
        selectedItem = 0
    elif(inputList()[pygame.K_1]):
        selectedItem = 1
    elif(inputList()[pygame.K_2]):
        selectedItem = 2
    elif(inputList()[pygame.K_3]):
        selectedItem = 3
    elif(inputList()[pygame.K_4]):
        selectedItem = 4
    elif(inputList()[pygame.K_5]):
        selectedItem = 5
    elif(inputList()[pygame.K_6]):
        selectedItem = 6
    elif(inputList()[pygame.K_7]):
        selectedItem = 7
    elif(inputList()[pygame.K_8]):
        selectedItem = 8
    elif(inputList()[pygame.K_9]):
        selectedItem = 9 

    else: 
        selectedItem = selectedItem

    return selectedItem

def placeItem(item, pos):
    instance = item(pos)
    return instance


while True: #Game Loop
    
    screen.fill((100, 100, 100))

    #Atualizações 
    clock.tick(60)
    playerPos = player.rect
    mousePos = pygame.mouse.get_pos()
    selectedTilePos = calcMouseTilePos(map)

    selectedItem = 0

    valid = validateTile((player.rect.x, player.rect.y), (selectedTilePos[0],selectedTilePos[1]), 42, "Tower")



    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Fecha o jogo
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Cria objeto no lugar do clique
            
            if selectedItem == 0:
                scoreText += 1

                if valid:
                    point = PointObj((selectedTilePos[0],selectedTilePos[1]))
                    pointList.append(point)

    if len(pointList) > 0:
        valid = validateTile((pointList[len(pointList)].rect.x, pointList[len(pointList)].rect.y), (selectedTilePos[0],selectedTilePos[1]),              42, "Player")


    if len(pointList) > 0: #move o player em direção ao objeto

        currentPoint = pointList[0]

        if player.rect.x < currentPoint.rect.x:
            playerVelocity[0] = player.playerSpeed
            playerVelocity[1] = 0
        elif player.rect.x > currentPoint.rect.x:
            playerVelocity[0] = -player.playerSpeed
            playerVelocity[1] = 0
        elif player.rect.y < currentPoint.rect.y:
            playerVelocity[0] = 0
            playerVelocity[1] = player.playerSpeed
        elif player.rect.y > currentPoint.rect.y:
            playerVelocity[0] = 0
            playerVelocity[1] = -player.playerSpeed
        else:
            playerVelocity[0] = 0
            playerVelocity[1] = 0

        if playerPos == point.rect:
            pointList.pop(0)

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

    if(inputList()[pygame.K_SPACE]):
        pauseGame = not pauseGame

    if pauseGame == False:
        playerRect, collisions = move(player.rect, playerVelocity, tileRects)

    else:
        playerRect = player.rect
    #region Score
    scoreTextSurface = font.render(str(scoreText), True, scoreTextColor)
    scoreTextRect = scoreTextSurface.get_rect()
    scoreTextRect.center = (100, 200)
    #endregion

    if pointList:
        pygame.draw.line(screen, (255, 0, 0), playerPos.center, (point.rect.centerx, point.rect.centery), 5)

    for point in pointList:
        screen.blit(point.image, (point.rect.x, point.rect.y))
    screen.blit(selectedTile, calcMouseTilePos(map))
    playerRotatedImg = pygame.transform.rotate(player.image, angle)
    screen.blit(playerRotatedImg, (playerRect.x, playerRect.y))
    possibleTiles(player.rect)


    pygame.display.update() #Atualiza a tela