import pygame
import sys

#region Inicio do codigo
pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Mánirius")
clock = pygame.time.Clock()
#endregion

#region Global Variables
verminVibes = "Fonts/Vermin Vibes 1989.ttf"
kenneyPixel = "Fonts/Kenney Pixel.ttf"
#endregion

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

class PointHandler():
    def __init__(self):

        super().__init__()
        self.pointSprite = pygame.image.load('Sprites/point.png').convert_alpha()
        self.pointList = []

    def AddPoint(self, position):
        point = PointObj(position)
        self.pointList.append(point)

    def DeletePoint(self,index):
        self.pointList.pop(index)

    def DrawPoints(self, screen, playerRect):
        if self.pointList:
            currentPoint = self.pointList[0]
            pygame.draw.line(screen, (255, 255, 255), playerRect.center, currentPoint.rect.center, 4)

            for a in range(len(self.pointList) - 1):
                pygame.draw.line(screen, (255, 255, 255), self.pointList[a].rect.center, self.pointList[a + 1].rect.center, 4)

        for point in self.pointList:
            screen.blit(point.image, (point.rect.x, point.rect.y))

    def Update(self, screen, playerRect, leftClick, rightClick, playMode, pauseGame):

        if playMode:
            if leftClick: 
                self.AddPoint(calcMouseTilePos())

            if rightClick:
                self.DeletePoint(len(self.pointList) - 1)

            if self.pointList:
                if playerRect.center == self.pointList[0].rect.center:
                    self.DeletePoint(0)

        self.DrawPoints(screen, playerRect)

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
        
    def Update(self, screen, pointHandler):

        if pointHandler.pointList:
            if self.rect.center == pointHandler.pointList[0].rect.center:
                pointHandler.DeletePoint(0)

        self.MovePlayer(pointHandler)
        self.DrawPlayer(screen)

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

def calcMouseTilePos():

    mousePosition = pygame.mouse.get_pos()

    tileX = mousePosition[0] // 64
    tileY = mousePosition[1] // 64

    tileX = tileX * 64
    tileY = tileY * 64

    return (tileX, tileY) 

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

def DrawText(text, font, fontSize, color, surface, x, y):
    fontObj = pygame.font.Font(font, fontSize)
    textObj = fontObj.render(text, 1, color)

    lines = text.splitlines()  # divide o texto em linhas
    for i, line in enumerate(lines):
        textObj = fontObj.render(line, 1, color)
        textRect = textObj.get_rect()
        textRect.center = (x, y + i*fontSize)  # ajusta a posição y para cada linha
        surface.blit(textObj, textRect)

class Button():
    def __init__(self, text, font, fontSize, textNormalColor, textHoverColor, normalColor, hoverColor, btnSize, pos, command):
        self.text = text
        self.textNormalColor = textNormalColor
        self.textHoverColor = textHoverColor
        self.font = font
        self.fontSize = fontSize
        self.btnSize = btnSize
        self.pos = pos
        self.normalColor = normalColor
        self.hoverColor = hoverColor
        self.command = command
        self.normalSurface = self.CreateSurface(self.textNormalColor, self.normalColor)
        self.hoverSurface = self.CreateSurface(self.textHoverColor, self.hoverColor)
        self.buttonRect = pygame.Rect(self.pos, self.btnSize)
    
    def CreateSurface(self, textColor, btnColor):
        surface = pygame.Surface(self.btnSize)
        surface.fill(btnColor)
        font = pygame.font.Font(self.font, self.fontSize)
        textObj = font.render(self.text, 1, textColor)
        textRect = textObj.get_rect(center = (self.btnSize[0] / 2, self.btnSize[1] / 2))
        surface.blit(textObj, textRect)
        return surface      

    def Update(self, surface, click):
        mouseX, mouseY = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(mouseX, mouseY):
            surface.blit(self.hoverSurface, self.pos)
            if click:
                print("sexo3")
                self.command()

        else:
            surface.blit(self.normalSurface, self.pos)
        
class Background():
    def __init__(self, backgroundSprite, screen, speed):
        self.backgroundSprite = backgroundSprite
        self.screen = screen
        self.speed = speed
        self.offset = [0, 0]

    def DrawBackground(self):
        bgX, bgY = self.backgroundSprite.get_size()
        screenX, screenY = self.screen.get_size()

        xRepeat = screenX // bgX + 2
        yRepeat = screenY // bgY + 2



        if self.speed[0] >= 0:
            self.offset[0] += self.speed[0]
            if self.offset[0] >= bgX:
                self.offset[0] = 0

        elif self.speed[0] < 0:
            self.offset[0] += self.speed[0]
            if self.offset[0] <= -bgX:
                self.offset[0] = 0

        if self.speed[1] >= 0:
            self.offset[1] += self.speed[1]
            if self.offset[1] >= bgY:
                self.offset[1] = 0
        
        elif self.speed[1] < 0:
            self.offset[1] += self.speed[1]
            if self.offset[1] <= -bgY:
                self.offset[1] = 0


        for x in range(xRepeat):
            for y in range(yRepeat):
                screen.blit(self.backgroundSprite, ((x * bgX) + self.offset[0], (y * bgY) + self.offset[1]))

def MainMenu():

    backgroundSprite = pygame.image.load("Sprites/background.jpg")
    background = Background(backgroundSprite, screen, [-1, -1])

    startButton = Button("START", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 300), Scene1)
    settingsButton = Button("SETTINGS", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 400), sys.exit)
    quitButton = Button("QUIT", kenneyPixel, 30, (255, 255, 255), (255, 255, 255), (58, 0, 85), (139, 40, 185), (200, 75), (220, 500), sys.exit)
    screenX, screenY = screen.get_size()
    click = False

    while True:
        screen.fill((0, 0, 0))

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

        #region Draw
        
        background.DrawBackground()

        #DrawText('MANIRIUS', verminVibes, 102, (255, 255, 0), screen, screenX / 2, 150)
        DrawText('MANIRIUS', verminVibes, 100, (255, 255, 255), screen, screenX / 2, 150)

        startButton.Update(screen, click)
        settingsButton.Update(screen, click)
        quitButton.Update(screen, click)

        #endregion

        pygame.display.update()
        clock.tick(60)

class Scene():
    def __init__(self, screen, clock, playerStartPos, mapArray):
        self.screen = screen
        self.clock = clock
        self.playerStartPos = playerStartPos
        self.mapArray = mapArray

        self.pointHandler = PointHandler()
        self.player = Player(self.playerStartPos)
        self.level = Level(mapArray, "Sprites/tileset.png", screen)
        
        self.playMode = False
        self.pauseGame = False

        self.inputs = {'space': False, 'rightClick': False, 'leftClick': False, 'escape': False, 'tab': False, 'one': False}

    def PauseGame(self, pause):
        self.pauseGame = pause
        
    def PlayMode(self, play):
        self.playMode = play

class Scene1(Scene):
    def __init__(self, screen, clock):
        playerStartPos = (64, 128)
        mapArray = [
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

        self.clock = clock
        self.screen = screen

        super().__init__(screen, clock, playerStartPos, mapArray)

    def Game(self):

        while True:
            screen.fill((0, 0, 0))

            #Atualizações de input

            for key in self.inputs: #reseta todos os inputs.
                self.inputs[key] = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Fecha o jogo
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN: #Apertar tecla
                    if event.key == pygame.K_0:
                        itemSelected = True

                    else:
                        itemSelected = False
                    
                    if event.key == pygame.K_SPACE:
                        self.inputs['space'] = True

                if event.type == pygame.MOUSEBUTTONDOWN: #Botão do mouse
                    
                    if event.button == 1:
                        self.inputs['leftClick'] = True

                    if event.button == 3:
                        self.inputs['rightClick'] = True    
                            
            #region Draw

            self.level.DrawLevel()

            #if itemSelected:
            #    if pointList:
            #        valid = validateTile(selectedTileTranslated, testPossibleTiles(pointList[len(pointList) - 1].rect))
            #        drawPossibleTiles(testPossibleTiles(pointList[len(pointList) - 1].rect)) 
            #        drawValidPoint(validateTile(selectedTileTranslated, testPossibleTiles(pointList[len(pointList) - 1].rect)), selectedTileTranslated)
            #    else:
            #        valid = validateTile(selectedTileTranslated, testPossibleTiles(playerPos))
            #        drawPossibleTiles(testPossibleTiles(player.rect))
            #        drawValidPoint(validateTile(selectedTileTranslated, testPossibleTiles(playerPos)), selectedTileTranslated)

            self.pointHandler.Update(self.screen, self.player.rect, self.inputs['leftClick'], self.inputs['rightClick'], True, True)
            self.player.Update(self.screen, self.pointHandler)

            #endregion

            self.clock.tick(60)
            pygame.display.update() #Atualiza a tela

class Scene2(Scene):
    def __init__(self, screen, clock):
        playerStartPos = (64, 128)
        mapArray = [
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

        self.clock = clock
        self.screen = screen

        super().__init__(screen, clock, playerStartPos, mapArray)

    def Game(self):

        while True:
            screen.fill((0, 0, 0))

            #Atualizações de input

            for key in self.inputs: #reseta todos os inputs.
                self.inputs[key] = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Fecha o jogo
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN: #Apertar tecla
                    if event.key == pygame.K_0:
                        itemSelected = True

                    else:
                        itemSelected = False
                    
                    if event.key == pygame.K_SPACE:
                        self.inputs['space'] = True

                if event.type == pygame.MOUSEBUTTONDOWN: #Botão do mouse
                    
                    if event.button == 1:
                        self.inputs['leftClick'] = True

                    if event.button == 3:
                        self.inputs['rightClick'] = True    
                            
            #region Draw

            self.level.DrawLevel()

            #if itemSelected:
            #    if pointList:
            #        valid = validateTile(selectedTileTranslated, testPossibleTiles(pointList[len(pointList) - 1].rect))
            #        drawPossibleTiles(testPossibleTiles(pointList[len(pointList) - 1].rect)) 
            #        drawValidPoint(validateTile(selectedTileTranslated, testPossibleTiles(pointList[len(pointList) - 1].rect)), selectedTileTranslated)
            #    else:
            #        valid = validateTile(selectedTileTranslated, testPossibleTiles(playerPos))
            #        drawPossibleTiles(testPossibleTiles(player.rect))
            #        drawValidPoint(validateTile(selectedTileTranslated, testPossibleTiles(playerPos)), selectedTileTranslated)

            self.pointHandler.Update(self.screen, self.player.rect, self.inputs['leftClick'], self.inputs['rightClick'], True, True)
            self.player.Update(self.screen, self.pointHandler)

            #endregion

            self.clock.tick(60)
            pygame.display.update() #Atualiza a tela
#region Heliópolis
#MainMenu()

scene1 = Scene1(screen, clock)
scene2 = Scene2(screen, clock)

scene2.Game()
#endregion