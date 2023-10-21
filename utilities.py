import pygame
import sys

def cutSpritesheet(spritesheet_path, sprite_width, sprite_height):
    # Carrega a spritesheet
    spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

    # Obtém as dimensões da spritesheet
    sheet_width, sheet_height = spritesheet.get_size()

    # Calcula o número de colunas e linhas de sprites na spritesheet
    columns = sheet_width // sprite_width
    rows = sheet_height // sprite_height

    # Cria uma lista para armazenar os sprites
    sprites = []

    # Percorre cada sprite na spritesheet
    for row in range(rows):
        for column in range(columns):
            # Calcula a posição do sprite na spritesheet
            x = column * sprite_width
            y = row * sprite_height

            # Corta o sprite da spritesheet
            sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))

            # Adiciona o sprite à lista de sprites
            sprites.append(sprite)

    return sprites

def calcMouseTilePos():

    mousePosition = pygame.mouse.get_pos()

    tileX = mousePosition[0] // 64
    tileY = mousePosition[1] // 64

    tileX = tileX * 64
    tileY = tileY * 64

    return (tileX, tileY) 

def inputCheck(inputs):
        
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

def collisionTest(rect , tiles):
    hitList = []
    for tile in tiles:
        if rect.colliderect(tile):
            hitList.append(tile)
    return hitList

def DrawText(text, font, fontSize, color, surface, x, y):
    fontObj = pygame.font.Font(font, fontSize)
    textObj = fontObj.render(text, 1, color)

    lines = text.splitlines()  # divide o texto em linhas
    for i, line in enumerate(lines):
        textObj = fontObj.render(line, 1, color)
        textRect = textObj.get_rect()
        textRect.center = (x, y + i*fontSize)  # ajusta a posição y para cada linha
        surface.blit(textObj, textRect)

def CheckUICollision(rect):
    mouseX, mouseY = pygame.mouse.get_pos()
    if rect.collidepoint(mouseX, mouseY):
        return True
    else:
        return False
    
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