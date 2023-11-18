import pygame, os, sys

def CutSpritesheet(spriteSheetPath, spriteSize):
    # Carrega a spritesheet
    spritesheet = pygame.image.load(spriteSheetPath).convert_alpha()

    # Obtém as dimensões da spritesheet
    sheet_width, sheet_height = spritesheet.get_size()

    # Calcula o número de colunas e linhas de sprites na spritesheet
    columns = sheet_width // spriteSize[0]
    rows = sheet_height // spriteSize[1]	

    # Cria uma lista para armazenar os sprites
    sprites = []

    # Percorre cada sprite na spritesheet
    for row in range(rows):
        for column in range(columns):
            # Calcula a posição do sprite na spritesheet
            x = column * spriteSize[0]
            y = row * spriteSize[1]

            # Corta o sprite da spritesheet
            sprite = spritesheet.subsurface(pygame.Rect(x, y, spriteSize[0], spriteSize[1]))

            # Adiciona o sprite à lista de sprites
            sprites.append(sprite)

    return sprites

def CalcMouseTilePos():

    mousePosition = pygame.mouse.get_pos()

    tileX = mousePosition[0] // 64
    tileY = mousePosition[1] // 64

    tileX = tileX * 64
    tileY = tileY * 64

    return (tileX, tileY) 

def EventCheck(inputs):
        
        for key in inputs: #reseta todos os inputs.
            inputs[key] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Fecha o jogo
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN: #Apertar tecla
                if event.key == pygame.K_1:
                    inputs['one'] = True
                
                if event.key == pygame.K_SPACE:
                    inputs['space'] = True

                if event.key == pygame.K_TAB:
                    inputs['tab'] = True

            if event.type == pygame.MOUSEBUTTONDOWN: #Botão do mouse
                
                if event.button == 1:
                    inputs['leftClick'] = True

                if event.button == 3:
                    inputs['rightClick'] = True 

def CollisionTest(rect , tiles):
    hitList = []
    for tile in tiles:
        if rect.colliderect(tile):
            hitList.append(tile)
    return hitList
    
def move(rect, movement, tiles):
    #collisionTypes = {'top': False, 'bottom': False, 'left': False, 'right': False}

    rect.x += movement[0] #MOVIMENTO HORIZONTAL

    hitList = CollisionTest(rect, tiles)
    for tile in hitList:
        if movement[0] > 0:
            rect.right = tile.left #caso haja colisão na direita, seta o jogador na posição da parte da esquerda do tile que colidiu.
            #collisionTypes['right'] = True

        elif movement[0] < 0:
            rect.left = tile.right #caso haja colisão na esquerda, seta o jogador na posição da parte da direita do tile que colidiu.
            #collisionTypes['left'] = True

    rect.y += movement[1] #MOVIMENTO VERTICA

    hitList = CollisionTest(rect, tiles)
    for tile in hitList:
        if movement[1] > 0: 
            rect.bottom = tile.top #caso haja colisão na parte debaixo, seta o jogador na posição da parte de cima do tile que colidiu.
            #collisionTypes['bottom'] = True

        if movement[1] < 0:
            rect.top = tile.bottom #caso haja colisão na parte de cima, seta o jogador na posição da parte debaixo do tile que colidiu.
            #collisionTypes['top'] = True
    return rect#, collisionTypes

def Animate(self, animation):
        self.sprites = CutSpritesheet(self.animations[animation]['spritesheet'], 64, 64)

        self.currentSprite += self.animations[animation] ['speed']

        if self.currentSprite > self.animations[animation] ['frames'] - 1:
            self.currentSprite = 0
            done = True

        else:
            done = False

        self.image = self.sprites[int(self.currentSprite)]
        return done

class Animator():
    def __init__(self, animations):
        self.animations = animations
        self.sprites = None
        self.speed = 1
        self.spriteIndex = 0
        self.done = False
    
    def GetAnimation(self):
        return self.sprites[int(self.spriteIndex)], self.done

    def Update(self):
        self.spriteIndex += self.speed

        if self.spriteIndex > len(self.sprites) - 1:
            self.spriteIndex = 0
            self.done = True

        else:
            self.done = False

    def SetAnimation(self, animation):
        self.sprites = CutSpritesheet(self.animations[animation]['spritesheet'], self.animations[animation]['size'])
        self.speed = self.animations[animation]['speed']

def LoadSprites(image_folder):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images = sorted(images, key=lambda img: int(img.split('_')[1].split('.')[0]))

    sprites = []
    for image in images:
        sprite = pygame.image.load(os.path.join(image_folder, image))
        sprites.append(sprite)

    return sprites